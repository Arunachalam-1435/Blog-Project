document.addEventListener('alpine:init', () => {
    Alpine.data('signupform', () => ({
            password: '',
            showPassword: false
        })
    );
});

const easyMDE = new EasyMDE({
    element: document.getElementById("body"),
    uploadImage: true,
    imageAccept: "image/png, image/jpeg, image/jpg, image/webp",
    previewImagesInEditor: true,
    imageUploadEndpoint: "/file"
});

async function submitPost(){
    var title = document.getElementById("topic").value;
    var content = easyMDE.value();
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

easyMDE.codemirror.on('change', () => {
    var md = easyMDE.value();
    var output = marked.parse(md);
    document.getElementById('output').innerHTML = output;
});