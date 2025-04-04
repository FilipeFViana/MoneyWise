const API_URL = "http://127.0.0.1:5000"; 


async function register(email, password) {
    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.status === 201) {
            alert("Usuário registrado com sucesso! Agora faça login.");
            window.location.href = "login.html";
        } else {
            alert(data.erro);
        }
    } catch (error) {
        console.error("Erro ao registrar usuário:", error);
    }
}


async function login(username, password) {
    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.access_token) {
            localStorage.setItem("token", data.access_token);
            alert("Login realizado com sucesso!");
            window.location.href = "dashboard.html"; // Redireciona para a página principal
        } else {
            alert("Usuário ou senha incorretos.");
        }
    } catch (error) {
        console.error("Erro ao fazer login:", error);
    }
}


async function carregarPerfil() {
    const token = localStorage.getItem("token");

    if (!token) {
        alert("Você precisa estar logado para acessar esta página!");
        window.location.href = "login.html"; // Redireciona para a página de login
        return;
    }

    try {
        const response = await fetch(`${API_URL}/perfil`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });

        const data = await response.json();
        document.getElementById("user-info").innerText = `Bem-vindo, ${data.mensagem}`;
    } catch (error) {
        console.error("Erro ao carregar perfil:", error);
        alert("Sessão expirada, faça login novamente.");
        localStorage.removeItem("token");
        window.location.href = "login.html";
    }
}

// Função para logout
function logout() {
    localStorage.removeItem("token");
    alert("Você saiu da sua conta!");
    window.location.href = "login.html";
}
