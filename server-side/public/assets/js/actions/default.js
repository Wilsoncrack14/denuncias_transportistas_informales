class User {
    constructor() {
        this.avatar = '';
        this.full_name = '';
        this.isSuperuser = false;
        this.currentUser = null;
    }

    init() {
        const data = localStorage.getItem('userData');
        if (data) {
            try {
                const user = JSON.parse(data);
                this.avatar = user.avatar || '';
                this.full_name = user.full_name || '';
                this.isSuperuser = user.is_superuser || false;
                this.currentUser = user;
            } catch (error) {
                console.error('Error al parsear userData:', error);
            }
        }
    }
}

document.addEventListener('alpine:init', () => {
    Alpine.data('currentUser', () => new User());
});
