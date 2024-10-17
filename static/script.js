$(document).ready(function () {
    function setdivcontent() {
        $.get("/getdata", function (data, status) {
            // Optionally, update the content div with new data
            $("#content").html(data);
            // Assuming data contains HTML
        });
    }

    const quill = new Quill("#editor", {
        modules: {
            syntax: true,
            toolbar: "#toolbar-container",
        },
        placeholder: "Compose an epic...",
        theme: "snow",
    });
    $('#clear-content').click(function() {
        $.post("/clearcontent", { command: 'clearcontent' });
    })
    $('#clear-editor').click(function() {
        quill.setContents([]);
    })
    quill.on('text-change', function(delta, oldDelta, source) {
        const imageBlots = quill.container.querySelectorAll('img');
        imageBlots.forEach((img) => {
            img.onclick = function () {
                const range = quill.getSelection();
                const index = quill.getIndex(img);
                quill.deleteText(index, 1);  // Delete the image from the editor
            };
        });
    });
    const toolbar = quill.getModule("toolbar");
    toolbar.addHandler("image", function () {
        const input = document.createElement("input");
        input.setAttribute("type", "file");
        input.setAttribute("accept", "image/*");
        input.click();
    
        $(input).on("change", function () {
            const file = input.files[0];
            const formData = new FormData();
            formData.append("file", file);
            
            // Replace '/upload' with your actual upload endpoint
            $.ajax({
                url: "/upload",
                type: "POST",
                data: formData,
                contentType: false,
                processData: false,
                success: function (result) {
                    // Assuming the server returns a URL
                    const imageUrl = result.url;
    
                    // Define your desired width and height
                    const width = "428px";  // Set desired width
                    const height = "432px"; // Set desired height
    
                    // Insert the image with specified width and height
                    const range = quill.getSelection();
                    quill.insertEmbed(range.index, 'custom-image', imageUrl);
    
                    // Use the Quill API to change the style after insertion
                    const imgElement = document.querySelector(`img[src="${imageUrl}"]`);
                    if (imgElement) {
                        imgElement.style.width = width;
                        imgElement.style.height = height;
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error("Error uploading image:", textStatus, errorThrown);
                },
            });
        });
    });

    $("#send").click(function () {
        const html = quill.getSemanticHTML(0, 1000);
        $.post("/datasend", { data: html });
        quill.setContents([]);
    });

    // Set an interval to call setdivcontent every 2 second
    setInterval(setdivcontent, 2000);
});