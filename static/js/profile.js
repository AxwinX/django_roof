// Client-side checks mirror the server-side validators (server is the source of truth).
(function () {
    const MAX_MB = 2;
    const MIN_DIM = 100;
    const MAX_DIM = 4000;
    const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];

    const input = document.getElementById("id_image");
    const preview = document.getElementById("avatar-preview");
    const placeholder = document.getElementById("avatar-placeholder");
    const errorEl = document.getElementById("client-error");
    const btn = document.getElementById("upload-btn");
    const form = document.getElementById("profile-image-form");
    if (!input) return;

    function fail(msg) {
        errorEl.textContent = msg;
        btn.disabled = true;
        input.value = "";
    }

    input.addEventListener("change", function () {
        errorEl.textContent = "";
        btn.disabled = true;
        const file = input.files[0];
        if (!file) return;

        if (!ALLOWED_TYPES.includes(file.type)) {
            return fail("Only JPG, PNG or WebP images are allowed.");
        }
        if (file.size > MAX_MB * 1024 * 1024) {
            return fail("Image is too large. Maximum size is " + MAX_MB + " MB.");
        }

        const url = URL.createObjectURL(file);
        const img = new Image();
        img.onload = function () {
            if (img.width < MIN_DIM || img.height < MIN_DIM) {
                URL.revokeObjectURL(url);
                return fail("Image is too small (" + img.width + "x" + img.height +
                            "). Minimum is " + MIN_DIM + "x" + MIN_DIM + " px.");
            }
            if (img.width > MAX_DIM || img.height > MAX_DIM) {
                URL.revokeObjectURL(url);
                return fail("Image is too large (" + img.width + "x" + img.height +
                            "). Maximum is " + MAX_DIM + "x" + MAX_DIM + " px.");
            }
            preview.src = url;
            preview.classList.remove("d-none");
            if (placeholder) placeholder.style.display = "none";
            btn.disabled = false;
        };
        img.onerror = function () {
            URL.revokeObjectURL(url);
            fail("This file is not a valid image.");
        };
        img.src = url;
    });

    form.addEventListener("submit", function (e) {
        if (!input.files.length) {
            e.preventDefault();
            errorEl.textContent = "Please choose an image to upload.";
        }
    });
})();
