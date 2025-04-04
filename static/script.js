const API_URL = "http://127.0.0.1:5000"; // URL DA API Flask


function mostrarErro(mensagem) {
    const erroDiv = document.getElementById("erro-mensagem");
    if (erroDiv) {
        erroDiv.innerText = mensagem;
        erroDiv.style.display = "block";
    } else {
        alert(mensagem);
    }
}

//  Validação do campo nome 
document.getElementById("name")?.addEventListener("input", function () {
    this.value = this.value.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, "");
});

//  Validação do campo CPF 
document.getElementById("cpf")?.addEventListener("input", function () {
    this.value = this.value.replace(/\D/g, "").slice(0, 11);
});

//  Cadastro de novo usuário
document.getElementById("register-form")?.addEventListener("submit", async function (event) {
    event.preventDefault();

    const nome = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const cpf = document.getElementById("cpf").value.trim();
    const senha = document.getElementById("password").value.trim();

    if (!/^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$/.test(nome)) {
        mostrarErro("O nome deve conter apenas letras.");
        return;
    }

    if (!/^\d{11}$/.test(cpf)) {
        mostrarErro("O CPF deve conter exatamente 11 números.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome, email, cpf, senha })
        });

        const data = await response.json();

        if (response.status === 201) {
            alert("Usuário registrado com sucesso!");
            window.location.href = "/login-page"; // Redireciona para login
        } else {
            mostrarErro(data.erro || "Erro ao cadastrar. Tente novamente.");
        }
    } catch (error) {
        mostrarErro("Erro de conexão com o servidor.");
    }
});

//  Login de usuário e armazenamento do token
document.getElementById("login-form")?.addEventListener("submit", async function (event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("password").value.trim();

    try {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (response.status === 200) {
            // Armazena o token no navegador
            localStorage.setItem("token", data.token);
            alert("Login realizado com sucesso!");
            window.location.href = "/dashboard"; // Redireciona para o painel
        } else {
            mostrarErro(data.erro || "E-mail ou senha inválidos.");
        }
    } catch (error) {
        mostrarErro("Erro ao se conectar com o servidor.");
    }
});
