import axios from 'axios';

const apiService = {
    fetchData: async () => {
    try {
        const response = await axios.get('/api/data');
        return response.data;
    } catch (error) {
        throw error;
    }
    },
};

export default apiService;