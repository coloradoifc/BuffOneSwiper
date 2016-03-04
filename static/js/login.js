 var EMAIL_REGEX = new RegExp(/^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i);

    $('#form').submit(function(evt) {
      evt.preventDefault();
      $('#error').html('');

      var password = $('#login-password').val();
      var email = $('#login-email').val();
      email = email ? email.trim() : null;

      if (!email && !password) {
        $('#error').html('Input credentials.');
        return;
      } else if (!email) {
        $('#error').html('Input email');
        return;
      } else if (!EMAIL_REGEX.test(email)) {
        $('#error').html('Invalid email');
        return;
      } else if (!password) {
        $('#error').html('Input password');
        return;
      }

      $.ajax({
        type: "POST",
        url: '/login',
        data: {
          email: email,
          password: password
        },
        success: function() {
          window.location.href = window.location.origin;
        },
        error: function() {
          $('#error').html('Incorrect email/password combination.');
          console.log('error.');
        }
      });
    });