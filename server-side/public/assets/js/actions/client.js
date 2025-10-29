export default class ApiClient {
    constructor() {
        this.error = {};
        this.success = '';
        this.loading = false;
        this.schema = null; 
        this.formFields = [];
    }

    clearMessages() {
        this.error = '';
        this.success = '';
    }

    resetForm() {
        this.formFields.forEach(field => this[field] = '');
    }

    async submit(endpoint, body = null, method = 'POST') {
        this.loading = true;
        this.clearMessages();

        try {
            const options = {
                method: method,
                headers: {
                    'Accept': 'application/json',
                    ...(localStorage.getItem('authToken') && { 'Authorization': `Token ${localStorage.getItem('authToken')}` }),
                },
            };

            if (method === 'GET' && body) {
                const params = new URLSearchParams(body);
                endpoint = `${endpoint}?${params.toString()}`;
            } 

            else if (body) {
                options.headers['Content-Type'] = 'application/json';
                options.body = JSON.stringify(body);
            }

            const response = await fetch(endpoint, options);
            const data = await response.json();

            if (!response.ok) {
                if (response.status === 400) {
                    this.error = data
                } else if (response.status === 500) {
                    this.error = {
                        non_field_errors: 'Server error. Please try again later.'
                    };
                }
                return { success: false, errors: this.error };
            }

            return { success: true, data };
        } catch (error) {
            console.error('API Error:', error);
            this.error = error.message;
            throw error;
        } finally {
            this.loading = false;
        }
    }

    async get(endpoint, params = null) {
        return await this.submit(endpoint, params, 'GET');
    }

    async post(endpoint, body = null) {
        return await this.submit(endpoint, body, 'POST');
    }

    async put(endpoint, body = null) {
        return await this.submit(endpoint, body, 'PUT');
    }

    async patch(endpoint, body = null) {
        return await this.submit(endpoint, body, 'PATCH');
    }

    async delete(endpoint, body = null) {
        return await this.submit(endpoint, body, 'DELETE');
    }
}