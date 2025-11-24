displayView = function(view){
  // the code required to display a view
  document.getElementById("current_view").innerHTML = view;
};
window.onload = function(){
  //TODO: Check for tokens and display correct view
  //clear_active_tabs();
  //document.getElementById("header_tabs").classList.remove("active");
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
    let welcome_view = document.getElementById('welcomeview').innerHTML;
    displayView(welcome_view);
    return;
  }
  let user_data = serverstub.getUserDataByToken(token);
  console.log("user data status: "+ user_data.success);
  if(user_data.success === false){
    let welcome_view = document.getElementById('welcomeview').innerHTML;
    displayView(welcome_view);
    return;
  }
  let profile_view = document.getElementById('profileview').innerHTML;
  displayView(profile_view);
  //User is already logged in. Setup home page...
  load_home_content(user_data);
  //document.getElementById('current_view').innerHTML= "";
  document.getElementById("header_tabs").classList.add("active");
  //document.getElementById("home_tab").classList.add("active");
  set_tab('home');
};

//NOTE: Global variables:
var min_pw = 5;


function validateEmail(email){
  return email.match(
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
}

function clear_active_tabs(){
  document.getElementById("home_view").classList.remove("active");
  document.getElementById("browse_view").classList.remove("active");
  document.getElementById("account_view").classList.remove("active");
  document.getElementById("home_tab").classList.remove("active");
  document.getElementById("browse_tab").classList.remove("active");
  document.getElementById("account_tab").classList.remove("active");

}

function set_tab(tab){
  let tab_view = tab + "_view";
  let tab_tab = tab + "_tab";
  clear_active_tabs();
  document.getElementById(tab_view).classList.add("active");
  document.getElementById(tab_tab).classList.add("active");
}

function login(form){
  let login_data = {
    email: form.email.value,
    password: form.password.value,
  };
  document.getElementById("welcome_forms_errors").innerHTML = "";
  if(validateEmail(login_data.email) == false){
    console.log("invalid email");
    document.getElementById("welcome_forms_errors").innerHTML = "Invalid Email";
    return;
  }
  if(login_data.password == "" || login_data.password.length < min_pw){
    console.log("invalid password");
    document.getElementById("welcome_forms_errors").innerHTML = "<p>" + "min password length: " + min_pw + "</p>";
    return;
  }

  let response = serverstub.signIn(login_data.email, login_data.password);
  if(response.success === false){
    document.getElementById("welcome_forms_errors").innerHTML = response.message;
  }
  //NOTE: Token now available.
  sessionStorage.setItem("token", response.data);
  form.reset();
  window.onload();
}

function sign_up(form){

  let signup_data ={
    email: form.email.value,
    password: form.password.value,
    password_check: form.password_check.value,
    fname: form.fname.value,
    lname: form.lname.value,
    gender: form.gender.value,
    country: form.country.value,
    city: form.city.value,
  };
  document.getElementById("welcome_forms_errors").innerHTML = "";
  if(validateEmail(signup_data.email) == false){
    console.log("invalid email");
    document.getElementById("welcome_forms_errors").innerHTML = "Invalid Email";
    return;
  }
  if(signup_data.password == "" || signup_data.password.length < min_pw){
    console.log("invalid password");
    document.getElementById("welcome_forms_errors").innerHTML = "<p>" + "min password length: " + min_pw + "</p>";
    return;
  }
  if((signup_data.password === signup_data.password_check) == false){
    console.log("passwords don't match");
    document.getElementById("welcome_forms_errors").innerHTML = "<p>" + "Passwords must match." + "</p>";
    return;
  }
  /*
        1. email
        2. password
        3. First name
        4. Family name
        5. gender
        6. city
        7. country
   * */
  let final_entry = {
    email: signup_data.email,
    password: signup_data.password,
    firstname: signup_data.fname,
    familyname: signup_data.lname,
    gender: signup_data.gender,
    city: signup_data.city,
    country: signup_data.country,
  };
  let response = serverstub.signUp(final_entry);
  if(response.success === false){
    document.getElementById("welcome_forms_errors").innerHTML = response.message;
  }
  //TODO: Login user and call window.onload etc.
  form.reset();
}


function change_password(form){
  let passwords={
    old_password: form.old_password.value,
    new_password1: form.new_password1.value,
    new_password2: form.new_password2.value,
  };
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){ //Not signed in 
    let welcome_view = document.getElementById('welcomeview').innerHTML;
    displayView(welcome_view);
    return;
  }
  if(passwords.new_password1 == "" || passwords.new_password1.length < min_pw){
    console.log("invalid password");
    document.getElementById("acc_error_msg").innerHTML = "<p>" + "min password length: " + min_pw + "</p>";
    return;
  }
  if((passwords.new_password1 === passwords.new_password2) == false){
    console.log("passwords don't match");
    document.getElementById("acc_error_msg").innerHTML = "<p>" + "Passwords must match." + "</p>";
    return;
  }
  
  let response = serverstub.changePassword(token, passwords.old_password, passwords.new_password1);
  //Doesn't matter if we changed password or not, just show the response...
  document.getElementById("acc_error_msg").innerHTML = response.message;
  form.reset();

}

function sign_out(){
  sessionStorage.removeItem("token");
  window.onload();
}

function load_home_content(user_data){
  //let user_data = serverstub.getUserDataByToken(token);
  console.log(user_data.data);
  //Object { email: "a@b.c", firstname: "zdfhsdfh", familyname: "adfh", gender: "male", city: "sdgd", country: "serhy" }
  let html_text = "";
  html_text += "<p>First name: " + user_data.data.firstname +"</p>";
  html_text += "<p>Family name: " + user_data.data.familyname +"</p>";
  html_text += "<p>Gender: " + user_data.data.gender +"</p>";
  html_text += "<p>Email: " + user_data.data.email +"</p>";
  html_text += "<p>City: " + user_data.data.city +"</p>";
  html_text += "<p>Country: " + user_data.data.country +"</p>";
  document.getElementById("personal_info").innerHTML = html_text;
  refresh_home_wall();
}

// home page 
function refresh_home_wall(){
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
    window.onload();
    return;
  }
  let response = serverstub.getUserMessagesByToken(token);
  if(response.success === false){
    window.onload();
    return;
  }
  let msg_html = "";
  for (let i = 0; i < response.data.length; i++) {
    msg_html += "<p>" + response.data[i].writer + ": " + response.data[i].content + "</p>";
  }
  document.getElementById("home_message_wall").innerHTML = msg_html;
}


function post_to_self(form){
  let full_text = "";
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
    window.onload();
    return;
  }
  let response = serverstub.getUserDataByToken(token);
  console.log(response);
  if(response.success === false){
    window.onload();
    return;
  }
  full_text += form.msg.value;
  console.log(full_text);
  serverstub.postMessage(token, full_text, response.data.email);
  form.reset();
  refresh_home_wall();
}

// browse user functions

var user_email = "";

function search_user(form) {  // ta in users mail
  console.log("TEST: " + form.email.value);
  let email = form.email.value;
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
    window.onload();
    return;
  }
  let user_mail = serverstub.getUserDataByToken(token);
  if (user_mail.success == false) {
    console.log("user does not exist");
    window.onload();
    return;
  }
  if(validateEmail(email) == false){
    document.getElementById("browse_error_msg").innerHTML = "Not a valid email";
    return;
  }
  let result = serverstub.getUserDataByEmail(token, email);
  if(result.success == false){
    document.getElementById("browse_error_msg").innerHTML = result.message;
    return;
  }
  let html_text = "";
  html_text += "<p>First name: " + result.data.firstname +"</p>";
  html_text += "<p>Family name: " + result.data.familyname +"</p>";
  html_text += "<p>Gender: " + result.data.gender +"</p>";
  html_text += "<p>Email: " + result.data.email +"</p>";
  html_text += "<p>City: " + result.data.city +"</p>";
  html_text += "<p>Country: " + result.data.country +"</p>";
  document.getElementById("user_info").innerHTML = html_text;
  user_email = result.data.email;
  refresh_user_wall();
}

function refresh_user_wall(){
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
    window.onload();
    return;
  }
  let response = serverstub.getUserMessagesByToken(token);
  if(response.success == false){
    window.onload();
    return;
  }
  response = serverstub.getUserMessagesByEmail(token, user_email);
  if(response.success == false){
    document.getElementById("browse_error_msg").innerHTML = result.message;
  }

  let msg_html = "";
  for (let i = 0; i < response.data.length; i++) {
    msg_html += "<p>" + response.data[i].writer + ": " + response.data[i].content + "</p>";
  }
  document.getElementById("user_message_wall").innerHTML = msg_html;

}

function post_to_user(form){
  let full_text = "";
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
    window.onload();
    return;
  }
  let response = serverstub.getUserDataByToken(token);
  console.log(response);
  if(response.success === false){
    window.onload();
    return;
  }

  if(user_email == ""){
    console.log("No user email.");
    document.getElementById("browse_error_msg").innerHTML = "No user email.";
    return;
  }

  console.log("post email: " + user_email);

  full_text += form.user_msg.value;
  console.log(full_text);
  response = serverstub.postMessage(token, full_text, user_email);
  if(response.success === false){
    document.getElementById("browse_error_msg").innerHTML = response.message;
    return;
  }
  document.getElementById("post_to_user").reset();
  refresh_user_wall();
}

