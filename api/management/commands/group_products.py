# from django.core.management.base import BaseCommand
# from collections import defaultdict
# from rapidfuzz import fuzz, process
# from api.models import Product, GroupProduct, Supermarket

# class Command(BaseCommand):
#     help = 'Groups similar products across supermarkets, one from each if possible, respecting product tiers.'

#     def handle(self, *args, **options):
#         # Define luxury and budget keywords
#         luxury_keywords = {
#             "Tesco": "finest",
#             "Sainsbury's": "taste the difference",
#             "ASDA": "extra special",
#             "Morrisons": "the best"
#         }
#         budget_keywords = {
#             "Tesco": "everyday",
#             "Sainsbury's": "stamford street",
#             "ASDA": "just essentials",
#             "Morrisons": "savers"
#         }

#         # Create initial groups
#         group_dict = {}
#         group_counter = 1
#         products = Product.objects.all().select_related('supermarket')

#         for product in products:
#             if product.groupproduct:  # Skip if already grouped
#                 continue
#             best_group = self.find_best_group(product, group_dict, luxury_keywords, budget_keywords)
#             if not best_group:
#                 best_group = GroupProduct.objects.create(common_product_name=f"Group {group_counter}")
#                 group_dict[best_group] = {product.supermarket.id: product}
#                 group_counter += 1
#             else:
#                 group_dict[best_group][product.supermarket.id] = product
#             product.groupproduct = best_group
#             product.save()

#     def find_best_group(self, product, group_dict, luxury_keywords, budget_keywords):
#         product_tier = self.get_product_tier(product.product_name, product.supermarket, luxury_keywords, budget_keywords)
#         for group, members in group_dict.items():
#             if product.supermarket.id in members:
#                 continue
#             for member in members.values():
#                 member_tier = self.get_product_tier(member.product_name, member.supermarket, luxury_keywords, budget_keywords)
#                 if member_tier == product_tier and self.is_match(product.product_name, member.product_name):
#                     return group
#         return None

#     def get_product_tier(self, product_name, supermarket, luxury_keywords, budget_keywords):
#         # Convert product name to lowercase for case-insensitive comparison
#         product_name_lower = product_name.lower()

#         # Get the supermarket-specific luxury and budget keywords and convert them to lowercase
#         luxury_keyword = luxury_keywords[supermarket.supermarket_name].lower()
#         budget_keyword = budget_keywords[supermarket.supermarket_name].lower()

#         # Check for luxury and budget keywords in the product name
#         if luxury_keyword in product_name_lower:
#             return 'luxury'
#         elif budget_keyword in product_name_lower:
#             return 'budget'
#         return 'mid-tier'  # Default tier if no specific keywords are found


#     def is_match(self, name1, name2):
#         words1 = set(name1.lower().split())
#         words2 = set(name2.lower().split())
#         intersection = words1.intersection(words2)
#         total = words1.union(words2)
#         match_percentage = len(intersection) / len(total) * 100
#         return match_percentage > 85  # Threshold for a significant match


from django.core.management.base import BaseCommand
from rapidfuzz import process, fuzz
from api.models import Product, GroupProduct, Supermarket

class Command(BaseCommand):
    help = 'Groups products by tier and only allows one entry per supermarket in each group.'

    def handle(self, *args, **options):
        products = Product.objects.all().select_related('supermarket')
        # Dictionary to track groups (group_id, tier)
        group_dict = {}

        for product in products:
            # Pass both product_name and supermarket to get_product_tier
            tier = self.get_product_tier(product.product_name, product.supermarket)
            key = (product.supermarket.id, tier)
            # Only groups that don't already have an entry from the supermarket and tier
            eligible_groups = [(g_id, grp) for (s_id, t), (g_id, grp) in group_dict.items() if s_id != product.supermarket.id and t == tier]
            existing_group = self.find_existing_group(eligible_groups, product.product_name)

            if existing_group:
                product.groupproduct = existing_group
            else:
                new_group = GroupProduct.objects.create(common_product_name=product.product_name)
                group_dict[(product.supermarket.id, tier)] = (new_group.id, new_group)
                product.groupproduct = new_group

            product.save()
            self.stdout.write(self.style.SUCCESS(f'Processed {product.product_name} in tier: {tier} for {product.supermarket.supermarket_name}'))

    def get_product_tier(self, product_name, supermarket):
        # Normalize the product name to lower case for case insensitive comparison
        product_name_lower = product_name.lower()

        # Define luxury and budget products specifically linked to the supermarket
        luxury_keywords = {
            "Tesco": "finest",
            "Sainsbury's": "taste the difference",
            "ASDA": "extra special",
            "Morrisons": "the best"
        }
        budget_keywords = {
            "Tesco": "everyday",
            "Sainsbury's": "stamford street",
            "ASDA": "just essentials",
            "Morrisons": "savers"
        }

        # Check for luxury tier keywords in the product name specific to the supermarket
        luxury_keyword = luxury_keywords.get(supermarket.supermarket_name, "").lower()
        if luxury_keyword and luxury_keyword in product_name_lower:
            return 'luxury'

        # Check for budget tier keywords in the product name specific to the supermarket
        budget_keyword = budget_keywords.get(supermarket.supermarket_name, "").lower()
        if budget_keyword and budget_keyword in product_name_lower:
            return 'budget'

        # General mid-tier classification for supermarket branded products without specific tier keywords
        if supermarket.supermarket_name.lower() in product_name_lower:
            return 'mid-tier'

        # Default to branded if none of the above conditions are met
        return 'branded'


    def find_existing_group(self, eligible_groups, product_name):
        name_to_group = {grp.common_product_name: grp for _, grp in eligible_groups}
        if not name_to_group:
            return None
        best_match = process.extractOne(product_name, name_to_group.keys(), scorer=fuzz.WRatio, score_cutoff=85)
        if best_match and best_match[1] > 80:
            return name_to_group[best_match[0]]
        return None


