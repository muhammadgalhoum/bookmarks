const siteUrl = "//127.0.0.1:8000/";
const styleUrl = siteUrl + "static/css/bookmarklet.css";
const minWidth = 300;
const minHeight = 300;

// Load CSS
var head = document.getElementsByTagName("head")[0]; // Get HTML head element
var link = document.createElement("link"); // Create new link Element
link.rel = "stylesheet"; // Set the attributes for link element
link.type = "text/css";
link.href = styleUrl + "?r=" + Math.floor(Math.random() * 9999999999999999);
head.appendChild(link); // Append link element to HTML head

// Load HTML
var body = document.getElementsByTagName("body")[0];
var boxHtml = `
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a>
        <h1>Select an image to bookmark:</h1>
        <div class="images"></div>
    </div>`;
body.innerHTML += boxHtml;

function bookmarkletLaunch() {
    var bookmarklet = document.getElementById("bookmarklet");
    var imagesFound = bookmarklet.querySelector(".images");

    // Clear images found
    imagesFound.innerHTML = "";
    // Display bookmarklet
    bookmarklet.style.display = "block";

    // Close event
    bookmarklet.querySelector("#close").addEventListener("click", function () {
        bookmarklet.style.display = "none";
    });

    // Find images in the DOM with the minimum dimensions
    var images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    images.forEach((image) => {
        if (image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
        var imageFound = document.createElement("img");
        imageFound.src = image.src;
        imagesFound.append(imageFound);
        }
    });

    // Select image event
    imagesFound.querySelectorAll("img").forEach((image) => {
        image.addEventListener("click", function (event) {
        var imageSelected = event.target;
        // Find the original image in the DOM that matches the selected image's src
        const originalImage = Array.from(images).find(
            (img) => img.src === imageSelected.src
        );
        // Use the title and alt attributes from the original image, or empty string if none
        const imageAlt = originalImage ? originalImage.alt : "Original Image has no alt value";
        const imageTitle = originalImage ? originalImage.title : "Original Image has no title value";
        bookmarklet.style.display = "none";
        window.open(
            siteUrl +
            "images/create/?url=" +
            encodeURIComponent(imageSelected.src) +
            "&title=" + encodeURIComponent(imageAlt) +
            "&description=" + encodeURIComponent(imageTitle),
            "_blank"
        );
        });
    });
}

// Launch the bookmarklet
bookmarkletLaunch();
