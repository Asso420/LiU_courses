//NOTE: Global variables:
var min_pw = 5;
var user_email = "";
let connection = {
  active: false,
  ws: null
};

function establish_connection(){
  let token = sessionStorage.getItem("token");
  let wsUrl = `ws://${window.location.host}/connect?token=${token}`;
  if(connection.active == null){
    return;
  }
  connection.ws = new WebSocket(wsUrl);

  connection.ws.onopen = function() {
    console.log("Got that connection :)");
    connection.active = true;
    
  };
  connection.ws.onclose = function() {
    console.log("Connection closed...");
    //sessionStorage.clear();
    connection.active = false;
    connection.ws = null;
    window.onload();
  };
  connection.ws.onerror = function() {
    console.log("websocket error.");
    sessionStorage.clear();
    connection.active = false;
    connection.ws = null;
    window.onload();
  };
  connection.ws.onmessage = function(event) {
    console.log("You've got mail.");
    let response = JSON.parse(event.data);
    console.log(response);
    switch (response.action){
      case "sign_out":
        console.log("SIGNING OUT!")
        sessionStorage.clear();
        connection.active = false;
        connection.ws = null;
        window.onload();
      default:
        console.log("UNKNOWN MESSAGE");
        break;
    }
  }
}

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
  //let user_data = serverstub.getUserDataByToken(token);
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      let user_data = JSON.parse(xhttp.responseText);
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

    }
  };
  xhttp.open("GET", "/get_user_data_by_token", true);
  xhttp.setRequestHeader("Authorization", token);
  xhttp.send();




};




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
    username: form.email.value,
    password: form.password.value,
  };
  document.getElementById("welcome_forms_errors").innerHTML = "";
  if(validateEmail(login_data.username) == false){
    console.log("invalid email");
    document.getElementById("welcome_forms_errors").innerHTML = "Invalid Email";
    return;
  }
  if(login_data.password == "" || login_data.password.length < min_pw){
    console.log("invalid password");
    document.getElementById("welcome_forms_errors").innerHTML = "<p>" + "min password length: " + min_pw + "</p>";
    return;
  }

  //let response = serverstub.signIn(login_data.email, login_data.password);

  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
       let response = JSON.parse(xhttp.responseText);
       console.log(response)
       if(response.success === false){
        if(this.status == 401){
          document.getElementById("welcome_forms_errors").innerHTML = "Wrong email or password";
          return;
        }else{
          document.getElementById("welcome_forms_errors").innerHTML = "Something went wrong";
        }
      }
      //NOTE: Token now available.
      sessionStorage.setItem("token", response.data);
      sessionStorage.setItem("email", login_data.username);
      establish_connection();
      form.reset();
      window.onload();
    }
  };
  xhttp.open("POST", "/sign_in", true);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(login_data));

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
  //let response = serverstub.signUp(final_entry);

  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
       let response = JSON.parse(xhttp.responseText);
       console.log(response)
       if(this.status == 409){
        document.getElementById("welcome_forms_errors").innerHTML = "The user already exist, pick a different username";
        return;
      }else if (this.status != 201){
        document.getElementById("welcome_forms_errors").innerHTML = "Something went wrong";
      }
    
      //TODO: Login user and call window.onload etc.
      form.reset();
    }
  };
  xhttp.open("POST", "/sign_up", true);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(final_entry));

/*
  if(response.success === false){
    document.getElementById("welcome_forms_errors").innerHTML = response.message;
  }
  //TODO: Login user and call window.onload etc.
  form.reset();
  */
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
  
  //let response = serverstub.changePassword(token, passwords.old_password, passwords.new_password1);
  let final_entry = {
    oldpassword: passwords.old_password,
    newpassword: passwords.new_password1,
    time: new Date().toISOString()
  };
  let hashed_entry = CryptoJS.HmacSHA256(JSON.stringify(final_entry), token).toString(CryptoJS.enc.Hex)
  console.log("unhashed string: " + JSON.stringify(final_entry))
  console.log("hash: " + hashed_entry)
  // console.log("entry: " + final_entry)
  let message = {
    data: final_entry,
    hash: hashed_entry
  };
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      let response = JSON.parse(xhttp.responseText);
      console.log(response)
      //Doesn't matter if we changed password or not, just show the response...
      if(this.status == 401){
        document.getElementById("acc_error_msg").innerHTML = "Wrong old password";
      }else if (this.status == 200){
        document.getElementById("acc_error_msg").innerHTML = "Password changed.";
      }else{
        document.getElementById("acc_error_msg").innerHTML = "Something went wrong.";
      }
      
      form.reset();
    }
  };
  xhttp.open("PUT", "/change_password", true);
  xhttp.setRequestHeader("Authorization", token);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(message));
 
 
  //Doesn't matter if we changed password or not, just show the response...
  //document.getElementById("acc_error_msg").innerHTML = response.message;
  //form.reset();

}

function sign_out(){

  let token = sessionStorage.getItem("token");
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      sessionStorage.clear();
      window.onload();
    }
  };
  xhttp.open("DELETE", "/sign_out", true);
  xhttp.setRequestHeader("Authorization", token);
  xhttp.send();
  
  

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
  //let response = serverstub.getUserMessagesByToken(token);

  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      let response = JSON.parse(xhttp.responseText);
      console.log("Refresh home wall: " + response)
      if(response.success === false){
        if(this.status == 500){
          document.getElementById("home_message_wall").innerHTML = "Server error, try again.";
        }else{
          window.onload();
          return;
        }

      }
      console.log("refresh user wall: " + response.data);
      let msg_html = "";
      for (let i = 0; i < response.data.length; i++) {
        msg_html += "<p>" + response.data[i][0] + ": " + response.data[i][1] + "</p>";
      }
      document.getElementById("home_message_wall").innerHTML = msg_html;
    }
  };
  xhttp.open("GET", "/get_user_messages_by_token", true);
  xhttp.setRequestHeader("Authorization", token);
  xhttp.send();
  
/*
  if(response.success === false){
    window.onload();
    return;
  }
  let msg_html = "";
  for (let i = 0; i < response.data.length; i++) {
    msg_html += "<p>" + response.data[i].writer + ": " + response.data[i].content + "</p>";
  }
  document.getElementById("home_message_wall").innerHTML = msg_html;
  */
}


function post_to_self(form){
  let full_text = "";
  let token = sessionStorage.getItem("token");
  let email = sessionStorage.getItem("email");
  console.log("token: "+ token);
  if(token === null){
    window.onload();
    return;
  }
  //let response = serverstub.getUserDataByToken(token);
  //console.log(response);

  let final_entry = {
    email: email,
    message: form.msg.value,
  };
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      let response = JSON.parse(xhttp.responseText);
      console.log("post to self: " + response)
      if(this.status == 500){
        document.getElementById("home_error_msg").innerHTML = "Server error, try again.";
      }else{
        window.onload();
        return;
      }
      form.reset();
      refresh_home_wall();
    }
  };
  xhttp.open("POST", "/post_message", true);
  xhttp.setRequestHeader("Authorization", token);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(final_entry));



}

// browse user functions



function search_user(form) {  // ta in users mail
  console.log("TEST: " + form.email.value);
  let email = form.email.value;
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
    window.onload();
    return;
  }

  if(validateEmail(email) == false){
    document.getElementById("browse_error_msg").innerHTML = "Not a valid email";
    return;
  }

  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      let result = JSON.parse(xhttp.responseText);
      if(result.success == false){
        if(this.status == 404){
          document.getElementById("browse_error_msg").innerHTML = "The user does not exist";
        }else{
          document.getElementById("browse_error_msg").innerHTML = "Something went wrong";
        }
        return;
      }
      document.getElementById("browse_error_msg").innerHTML = result.message;
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
  };
  xhttp.open("GET", "/get_user_data_by_email/" + email, true);
  xhttp.setRequestHeader("Authorization", token);
  xhttp.send();
}

function refresh_user_wall(){
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
    window.onload();
    return;
  }
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      let response = JSON.parse(xhttp.responseText);
      console.log("refresh user wall: " + response);
      if(response.success == false){
        if(this.status == 404){
          document.getElementById("browse_error_msg").innerHTML = "The user does not exist";
        }else{
          document.getElementById("browse_error_msg").innerHTML = "Something went wrong";
        }        return;
      }
      console.log("refresh user wall: " + response.data);
      let msg_html = "";
      for (let i = 0; i < response.data.length; i++) {
        msg_html += "<p>" + response.data[i][0] + ": " + response.data[i][1] + "</p>";
      }
      document.getElementById("user_message_wall").innerHTML = msg_html;
    }
  };
  xhttp.open("GET", "/get_user_messages_by_email/" + user_email, true);
  xhttp.setRequestHeader("Authorization", token);
  xhttp.send();

}

function post_to_user(form){
  let full_text = "";
  let token = sessionStorage.getItem("token");
  console.log("token: "+ token);
  if(token === null){
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

  let final_entry = {
    email: user_email,
    message: form.user_msg.value,
  };
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4) {
      let response = JSON.parse(xhttp.responseText);
      console.log("post to user: " + response)
      if(this.status == 500){
        document.getElementById("browse_error_msg").innerHTML = "Server error, try again.";
      }
      form.reset();
      refresh_user_wall();
    }
  };
  xhttp.open("POST", "/post_message", true);
  xhttp.setRequestHeader("Authorization", token);
  xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhttp.send(JSON.stringify(final_entry));
}

