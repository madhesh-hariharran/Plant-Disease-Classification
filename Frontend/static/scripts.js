// Get buttons, preview element
const captureButton = document.getElementById('capture-button');
const uploadButton = document.getElementById('upload-button');
const imagePreview = document.getElementById('image-preview');

// Capture photo from camera
captureButton.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const video = document.createElement('video');
        video.srcObject = stream;
        video.addEventListener('loadedmetadata', () => {
            video.play();
        });

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0);

        const imageData = canvas.toDataURL('image/jpeg');
        uploadImage(imageData);
    } catch (error) {
        console.error('Error capturing photo:', error);
        // Handle error gracefully (e.g., display a message to the user)
    }
});

// Open file selection dialog
uploadButton.addEventListener('click', () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = 'image/*';
    fileInput.style.display = 'none'; // Hide input visually
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (!file) {
            return; // User canceled or no file selected
        }

        validateAndUploadImage(file);
    });
    fileInput.click(); // Simulate click to open dialog
});

// Upload image data to Flask backend
async function uploadImage(imageData) {
    var fdata = new FormData();

    fdata.append('file', imageData);

    try {
        const response = await fetch('http://localhost:5000/', {
            method: 'POST',
            body: fdata,
        });
        const data = await response.json();
        // Handle response from backend (e.g., display success or error message)
        console.log(data);
    } catch (error) {
        console.error('Error uploading image:', error);
        // Handle upload error gracefully
    }
}

// Validate and upload file from gallery
async function validateAndUploadImage(file) {
    // Check file type (using Blob API or File object methods)
    const acceptedTypes = ['image/jpeg', 'image/png'];
    if (!acceptedTypes.includes(file.type)) {
        return alert('Invalid file type. Please choose an image file (JPEG or PNG).');
    }

    // Check file size (optional)
    const maxSize = 2 * 1024 * 1024; // 2 MB
    if (file.size > maxSize) {
        return alert('File size exceeds limit. Please choose a file smaller than 2 MB.');
    }

    // Read file as base64
    const reader = new FileReader();
    reader.onload = () => {
        uploadImage(reader.result);
    };
    reader.readAsDataURL(file);
}
