document.addEventListener('alpine:init', () => {
    Alpine.data('signupform', () => ({
            password: '',
            showPassword: false
        })
    );
});

const easyMDE = new EasyMDE({
    element: document.getElementById("body")
});

function submitPost(){
    console.log("hello world");
}

easyMDE.codemirror.on('change', () => {
    var md = easyMDE.value();
    var output = marked.parse(md);
    document.getElementById('output').innerHTML = output;
});