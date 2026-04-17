document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileDetails = document.getElementById('file-details');
    const passwordInput = document.getElementById('password');
    const togglePwdBtn = document.getElementById('toggle-pwd');
    const btnGenerate = document.getElementById('btn-generate');
    const btnProcess = document.getElementById('btn-process');
    const tabs = document.querySelectorAll('.tab-btn');
    const strengthMeter = document.getElementById('strength-meter');
    const strengthFill = document.getElementById('strength-fill');
    const strengthText = document.getElementById('strength-text');
    const statusMessage = document.getElementById('status-message');

    let currentAction = 'encrypt';
    let selectedFile = null;

    // Tab Switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentAction = tab.dataset.action;
            
            if (currentAction === 'encrypt') {
                btnProcess.querySelector('span').textContent = 'Encrypt & Save PDF';
                btnProcess.classList.remove('decrypt-mode');
                strengthMeter.classList.remove('hidden');
                btnGenerate.classList.remove('hidden');
            } else {
                btnProcess.querySelector('span').textContent = 'Decrypt & Save PDF';
                btnProcess.classList.add('decrypt-mode');
                strengthMeter.classList.add('hidden');
                btnGenerate.classList.add('hidden');
            }
        });
    });

    // File Drag & Drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        let files = e.dataTransfer.files;
        handleFiles(files);
    }, false);

    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
                showStatus('Please select a valid PDF file.', true);
                return;
            }
            selectedFile = file;
            const size = (file.size / (1024 * 1024)).toFixed(2);
            fileDetails.textContent = `Selected: ${file.name} (${size} MB)`;
            fileDetails.classList.remove('hidden');
            hideStatus();
        }
    }

    // Password Toggle
    togglePwdBtn.addEventListener('click', () => {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
    });

    // Password Strength Checker
    let typingTimer;
    passwordInput.addEventListener('input', () => {
        clearTimeout(typingTimer);
        const pwd = passwordInput.value;
        
        if (currentAction === 'encrypt') {
            if (pwd.length === 0) {
                strengthMeter.classList.add('hidden');
                return;
            }
            strengthMeter.classList.remove('hidden');
            
            typingTimer = setTimeout(async () => {
                try {
                    const res = await fetch('/api/analyze_password', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ password: pwd })
                    });
                    const data = await res.json();
                    strengthText.textContent = data.strength;
                    
                    let width = '33%';
                    let bg = '#F44336'; // Weak
                    if (data.strength === 'Medium') { width = '66%'; bg = '#FF9800'; }
                    if (data.strength === 'Strong') { width = '100%'; bg = '#4CAF50'; }
                    
                    strengthFill.style.width = width;
                    strengthFill.style.backgroundColor = bg;
                    strengthText.style.color = bg;
                } catch (e) {
                    console.error('Analyzation failed', e);
                }
            }, 300);
        }
    });

    // Generate Password
    btnGenerate.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/generate_password');
            const data = await res.json();
            passwordInput.value = data.password;
            passwordInput.setAttribute('type', 'text');
            passwordInput.dispatchEvent(new Event('input')); // Trigger strength checker
            
            setTimeout(() => {
                passwordInput.setAttribute('type', 'password');
            }, 3000);
        } catch (e) {
            console.error(e);
        }
    });

    // Process Submission
    btnProcess.addEventListener('click', async () => {
        if (!selectedFile) {
            showStatus('Please drop a PDF file first.', true);
            return;
        }
        if (!passwordInput.value) {
            showStatus('Please enter a password.', true);
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('password', passwordInput.value);
        formData.append('action', currentAction);

        btnProcess.querySelector('span').textContent = 'Processing...';
        btnProcess.classList.add('disabled');
        btnProcess.disabled = true;
        hideStatus();

        try {
            const res = await fetch('/api/process', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();

            if (res.ok && data.success) {
                showStatus(`${currentAction === 'encrypt' ? 'Encryption' : 'Decryption'} successful! Initiating download...`, false);
                window.location.href = data.download_url;
            } else {
                showStatus(data.error || 'Processing failed.', true);
            }
        } catch (error) {
            showStatus('A network error occurred. Please try again.', true);
        } finally {
            btnProcess.querySelector('span').textContent = currentAction === 'encrypt' ? 'Encrypt & Save PDF' : 'Decrypt & Save PDF';
            btnProcess.disabled = false;
        }
    });

    function showStatus(text, isError) {
        statusMessage.textContent = text;
        statusMessage.className = `status-message ${isError ? 'status-error' : 'status-success'}`;
    }

    function hideStatus() {
        statusMessage.className = 'status-message hidden';
    }
});
