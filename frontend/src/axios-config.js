import axios from 'axios';

// Set the base URL for all Axios requests
// Adjust this URL to match your Django backend server address
axios.defaults.baseURL='http://127.0.0.1:8000/';

// Allow cookies to be sent with requests (important for session-based authentication)
axios.defaults.withCredentials = true;

// Get CSRF token from the cookie named 'csrftoken' and set it in the common headers
// This is necessary for Django's CSRF protection to accept the requests from Axios
function getCsrfToken() {
  let csrfToken = '';
  const csrfCookie = document.cookie.split(';').find(cookie => cookie.trim().startsWith('csrftoken='));
  if (csrfCookie) {
    csrfToken = csrfCookie.split('=')[1];
  }
  return csrfToken;
}

axios.defaults.headers.common['X-CSRFToken'] = getCsrfToken();

// Export the configured Axios to be used in your Vue components
export default axios;






// Hi, Paulo. I'm a final year undergrad student, I was in your Web Programming module. I enjoyed it a lot and decided that I would use Django and Vue for my final year project dissertation. I changed the Typescript setup to Javascript. However, I am having an issue with rendering the frontend. I wanted to ask whether you could help. Please can you let me know y