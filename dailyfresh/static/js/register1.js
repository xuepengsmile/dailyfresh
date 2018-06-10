$(function () {
    // 错误falg
    error_name = false;
    error_pwd= false;
    error_=cpwd = false;
    error_email = false;
    error_check = false;

    
// 失焦点调函数
    $('#user_name').blur(function(){
        check_username();
    });
    $('#pwd').blur(function(){
        check_pwd();
    });
    $('#cpwd').blur(function(){
        check_cpwd();
    });
    $('#email').blur(function(){
        check_email();
    });
    $('#allow').click(function(){
        if($(this).is(':checked')){
            $(this).next().hide();
            error_check = true;
        }
        else{
            $(this).next().text('请勾选同意').show;
            error_check = false;
        }
    });

    
    //写函数
    function check_username() {
       var len = $('#user_name').val().length;
       if(len<5 || len>20){
           $('#user_name').next().text('请输入5-20个字符').show();
           error_name = false;
       }
       else{
           $.get('/user/register_exit/?username='+$('#user_name').val(), function (data) {
               if(data.count==1){
                   $('#user_name').next().text('该用户已存在').show();
                   error_name = false;
               }
               else{
                   $('#user_name').next().hide();
                   error_name = true;
               }
           })
       }
    }

    function check_pwd() {
        var len = $('#pwd').val().length;
        if(len<4||len>20){
            $('#pwd').next().text('密码请输入4-20字符').show();
            error_pwd = false
        }
        else{
            $('#pwd').next().hide();
            error_pwd = true;
        }
    }

    function check_cpwd() {
        var pwd = $('#pwd').val();
        var cpwd = $('#cpwd').val();
        if(pwd != cpwd){
            $('#cpwd').next().text('请输入相同的密码').show();
            error_pwd = false
        }
        else{
            $('#cpwd').next().hide();
            error_pwd = true;
        }
    }


    function check_email() {
        var re = /^[0-9a-z][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
        if(re.test($('#email').val())){
            $('#email').next().hide();
            error_pwd = true;
        }
        else{
            $('#email').next().text('邮箱格式不正确').show();
            error_pwd = false
        }
    }
});