function checkForm(form)
{
  if(form.password.value != form.cpassword.value){
    alert("UH-OH! Your passwords do not match! Please re-enter your passwords so they match!")
    return false;
  }
}
