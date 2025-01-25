document.getElementById('metadataForm').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(this);
    const progressContainer = document.getElementById('progressContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const downloadLink = document.getElementById('downloadLink');
    const loadingSpinner = document.getElementById('loadingSpinner');

    // Reset progress
    progressContainer.style.display = 'block';
    progressBar.style.width = '0';
    progressText.textContent = 'Proses dimulai...';
    downloadLink.style.display = 'none';
    loadingSpinner.style.display = 'flex';

    try {
        // Simulasi progres
        let progress = 0;
        const interval = setInterval(() => {
            if (progress < 90) {
                progress += 10;
                progressBar.style.width = `${progress}%`;
                progressText.textContent = `Proses berlangsung... ${progress}%`;
            }
        }, 500);

        // Simulasi permintaan server
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        clearInterval(interval);
        loadingSpinner.style.display = 'none';

        if (response.ok) {
            const data = await response.json();
            progressBar.style.width = '100%';
            progressText.textContent = 'Proses selesai!';
            downloadLink.style.display = 'block';
            downloadLink.href = data.download_url;
            downloadLink.textContent = 'Unduh File';
        } else {
            const error = await response.json();
            alert(error.error || 'Terjadi kesalahan saat mengunggah file.');
        }
    } catch (error) {
        loadingSpinner.style.display = 'none';
        alert(`Terjadi kesalahan: ${error.message || 'Gagal memproses file.'}`);
    }
});

// Preview Gambar
document.getElementById('images').addEventListener('change', function () {
    const files = this.files;
    const previewContainer = document.getElementById('previewContainer');
    previewContainer.innerHTML = '';

    Array.from(files).forEach((file) => {
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        }
    });
});
