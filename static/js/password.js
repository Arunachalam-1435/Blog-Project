document.addEventListener('alpine:init', () => {
    Alpine.data('signupform', () => ({
            password: '',
            showPassword: false
        })
    );
});