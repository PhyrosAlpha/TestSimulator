let save_btn = document.getElementById("save-btn");
let csrf_token = document.getElementsByName("csrfmiddlewaretoken")[0];
let textarea = document.getElementById("annotation-id");
let select = document.getElementById("tag-id");
let toastElement = document.getElementById("toast");
let toast = new bootstrap.Toast(toastElement);

save_btn.addEventListener("click", () => {
    let value = textarea.value;
    let csrfValue = csrf_token.value;
    let tagValue = select.value;

    let formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrfValue);
    formData.append("annotation", value);
    formData.append("tag", tagValue);

    fetch(`${window.location.href}save/`, {
        method: "POST",
        body: formData
    })
    .then(response => {
        response.json().then(data => console.log(data)); 
        toast.show();
    });
});

