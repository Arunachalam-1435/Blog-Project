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
        
        if (!response.ok){
            throw new Error(`Server returnded ${response}`);
        }
        const data = await response.json();
        console.log("Post saved", data);
    }
    catch(err){
        console.error("Failed to send post");
    }
}

easyMDE.codemirror.on('change', () => {
    var md = easyMDE.value();
    var output = marked.parse(md);
    document.getElementById('output').innerHTML = output;
});