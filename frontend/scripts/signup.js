const signup_form = document.querySelector(".signup-form")
signup_form.addEventListener("submit",(event)=>{
    event.preventDefault()

    let has_error = false

    const email = document.querySelector("#email").value
    const pass = document.querySelector(".pass").value
    const cnf_pass = document.querySelector(".cnf-pass").value



    console.log("Email we got is :",email)
    console.log(`pass is ${pass} and cnf pass is ${cnf_pass}`)
    let is_valid_email = check_email(email)
    let is_both_pass_same = check_pass(pass,cnf_pass)
    
    if(!is_valid_email){
        const invld_email_alert = document.querySelector(".invld-email")
        invld_email_alert.classList.remove("hidden")
        has_error = true
    }

    if(!is_both_pass_same){
        const invld_pass = document.querySelector(".invld-pass")
        invld_pass.classList.remove("hidden")
        has_error = true
    }
    
    if (!has_error){
        const signup_status = do_signup()
    }
    


})





function check_email(email) {
    if(!email.includes("@")){
        return false
    }
    return true
}

function check_pass(pass,cnf_pass){
    if (pass!= cnf_pass){
        return false
    }
    return true
}

function do_signup(email,pass){
    const signup_api = ""
}

document.querySelector("#email").addEventListener("input",()=>{
    document.querySelector(".invld-email").classList.add("hidden")
})

document.querySelector(".pass").addEventListener("input",()=>{
    document.querySelector(".invld-pass").classList.add("hidden")
})


const buttons = document.querySelectorAll(".pass-btn1,.pass-btn2").addEventListener("click",()=>{

    buttons.foreach((button)=>{

    console.log("show pass btn clicked")
    const pass_type = document.querySelector(".pass")
    console.log("pass type is ",pass_type)
    if (pass_type.type === "password"){
        pass_type.type = "text"
        document.querySelector(".fa-eye-slash").style.display = "none"
        document.querySelector(".fa-eye").style.display = "block"
    }

    else if(pass_type.type === "text"){
        pass_type.type = "password"
        document.querySelector(".fa-eye-slash").style.display = "block"
        document.querySelector(".fa-eye").style.display = "none"
    }

    })
   

})