async function submit_login_form(event){
    event.preventDefault()
    let email_filed = document.getElementById("email")
    let password_filed = document.getElementById("password")

    let email = email_filed.value;
    let password = password_filed.value;


    console.log(`get_login_form called with email as ${email} and password as ${password}`)


    let login_url = "http://127.0.0.1:8000/auth/login"
    let user_info = { "email" : email, "password" : password}

    try{

        const response =  await fetch(login_url,
            {
            method:"POST",
            headers: {"Content-Type": "application/json"},
            body:JSON.stringify(user_info)
        }
        );

        if(!response.ok){
            console.log("Login error")
        }

        const data = await response.json();
        console.log("reposne of api is", data.msg);
        if(data.msg == "success"){
            localStorage.setItem("jwt", data.token);
        }
        

    }
    catch(error){
        console.log(`Error got during login ${error}`)
    }

}

document
    .getElementById("login-form")
    .addEventListener("submit",submit_login_form)


