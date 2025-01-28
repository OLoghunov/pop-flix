async function checkUserAuthentication() {
    const navbarButtons = document.querySelector('.navbar .buttons');
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        navbarButtons.innerHTML = `
            <button class="button" id="register-button">Регистрация</button>
            <button class="button" id="login-button">Вход</button>
        `;
        setupAuthButtons();
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/api/0.1/auth/me', {
            method: 'GET',
            headers: { Authorization: `Bearer ${accessToken}` },
        });

        if (!response.ok) {
            throw new Error('Invalid token');
        }

        const userData = await response.json();

        navbarButtons.innerHTML = `
            <a href="profile.html" class="button" id="profile-button">Привет, ${userData.username}</a>
        `;
    } catch (error) {
        console.error('Ошибка проверки токена:', error);

        localStorage.removeItem('access_token');
        navbarButtons.innerHTML = `
            <button class="button" id="register-button">Регистрация</button>
            <button class="button" id="login-button">Вход</button>
        `;
        setupAuthButtons();
    }
}

function setupAuthButtons() {
    document.getElementById('register-button').addEventListener('click', () => {
        const redirectUrl = window.location.href;
        window.location.href = `register.html?redirect=${encodeURIComponent(redirectUrl)}`;
    });

    document.getElementById('login-button').addEventListener('click', () => {
        const redirectUrl = window.location.href;
        window.location.href = `login.html?redirect=${encodeURIComponent(redirectUrl)}`;
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const token = localStorage.getItem("access_token");
    const buttonsContainer = document.querySelector(".buttons");

    if (token) {
        buttonsContainer.innerHTML = `
            <div class="profile-menu-container">
                <button class="button profile-button">Профиль</button>
                <div class="profile-menu hidden">
                    <button class="menu-item" id="go-to-profile">Перейти в профиль</button>
                    <button class="menu-item" id="logout-button">Выйти</button>
                </div>
            </div>
        `;

        const profileButton = document.querySelector(".profile-button");
        const profileMenu = document.querySelector(".profile-menu");

        profileButton.addEventListener("click", () => {
            profileMenu.classList.toggle("hidden");
        });

        document.getElementById("go-to-profile").addEventListener("click", () => {
            window.location.href = "/profile.html";
        });

        document.getElementById("logout-button").addEventListener("click", () => {
            localStorage.removeItem("access_token");
            window.location.reload();
        });
    }
});

