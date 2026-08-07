document.addEventListener('alpine:init', () => {
    Alpine.data('signupform', () => ({
            password: '',
            showPassword: false
        })
    );
});

var editor = document.getElementById("body");
var submit = document.getElementById("submit");

submit.addEventListener("click", function (){
    submitPost();
});

async function submitPost(){
    var title = document.getElementById("topic").value;
    var content = editor.value;
    if (title === "" || content === ""){
        alert("Please fill title of the blog and its content");
        return;
    }
    try{
        const response = await fetch("/post", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                topic: title,
                body: content
            })
        });
        const data = await response.json();
        if (data.redirect_url){
            window.location.href = data.redirect_url;
        }
    }
    catch(err){
        console.error("Failed to send post\n", err);
    }
}

editor.addEventListener("input", function() {
    var md = editor.value;
    var html = marked.parse(md);
    var out = document.getElementById("output");
    out.innerHTML = html;
    out.scrollTop = out.scrollHeight;
});