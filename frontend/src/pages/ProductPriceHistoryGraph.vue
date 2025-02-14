<!-- <template>
    <div>
      <vue-line-chart :chart-data="chartData" :options="chartOptions" />
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { VueLineChart } from 'vue3-charts';
  import axios from 'axios';
  
  export default {
    components: {
      VueLineChart
    },
    props: {
      groupId: Number
    },
    setup(props) {
      const chartData = ref({
        datasets: []
      });
      const chartOptions = ref({
        responsive: true,
        scales: {
          x: {
            type: 'time',
            time: {
              tooltipFormat: 'DD MMM YYYY',
              unit: 'day'
            }
          },
          y: {
            beginAtZero: true
          }
        },
        plugins: {
          tooltip: {
            callbacks: {
              label: function(context) {
                let label = `${context.dataset.label}: £${context.raw.y}`;
                if (context.raw.salePrice === context.raw.y) {
                  label += ` - Sale (£${context.raw.salePrice}) ${context.raw.saleDeal || ''}`;
                } else if (context.raw.loyaltyPrice === context.raw.y) {
                  label += ` - Loyalty Card (£${context.raw.loyaltyPrice}) ${context.raw.loyaltyDeal || ''}`;
                } else {
                  label += ` - RRP (£${context.raw.rrp})`;
                }
                return label;
              }
            }
          }
        },
        elements: {
          line: {
            tension: 0.4
          },
          point: {
            radius: 5
          }
        }
      });
  
      function getColorBySupermarket(supermarket) {
        switch (supermarket) {
          case 'Tesco': return '#000080';
          case 'Sainsbury\'s': return '#FFA500';
          case 'Asda': return '#32CD32';
          case 'Morrisons': return '#006400';
          default: return '#cccccc';
        }
      }
  
      const processChartData = (data) => {
        const datasets = data.map(item => ({
          label: item.product_name + ' (' + item.supermarket_name + ')',
          borderColor: getColorBySupermarket(item.supermarket_name),
          data: item.price_history.map(ph => ({
            x: ph.datetime_price_updated,
            y: Math.min(ph.rrp_price, ph.sale_price || Infinity, ph.loyalty_card_price || Infinity),
            rrp: ph.rrp_price,
            salePrice: ph.sale_price,
            saleDeal: ph.sale_deal,
            loyaltyPrice: ph.loyalty_card_price,
            loyaltyDeal: ph.loyalty_card_deal
          }))
        }));
        chartData.value.datasets = datasets;
      };
  
      const fetchChartData = async () => {
        try {
          const response = await axios.get(`/price-history/${props.groupId}`);
          processChartData(response.data);
        } catch (error) {
          console.error('Error fetching data: ', error);
        }
      };
  
      onMounted(fetchChartData);
  
      return {
        chartData,
        chartOptions
      };
    }
  };
  </script>
   -->