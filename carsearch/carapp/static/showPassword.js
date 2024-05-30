function showPassword(e){
    var input = document.getElementById('password1')
    if(input.type == 'password'){
      input.type = "text"
      e.target.className = "bi bi-eye-fill"
    }else{
      input.type = "password"
      e.target.className = "bi bi-eye-slash-fill"
    }
  }

  function showPassword2(e){
    var input2 = document.getElementById('password2')
    if(input2.type == 'password'){
      input2.type = "text"
      e.target.className = "bi bi-eye-fill"
    }else{
      input2.type = "password"
      e.target.className = "bi bi-eye-slash-fill"
    }
  }

function showPasswordLogin(e){
    var input = document.getElementById('password')
    if(input.type == 'password'){
      input.type = "text"
      e.target.className = "bi bi-eye-fill"
    }else{
      input.type = "password"
      e.target.className = "bi bi-eye-slash-fill"
    }
  }