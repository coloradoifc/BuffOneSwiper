var EMAIL_REGEX = new RegExp(/^[-a-z0-9~!$%^&*_=+}{\'?]+(\.[-a-z0-9~!$%^&*_=+}{\'?]+)*@([a-z0-9_][-a-z0-9_]*(\.[-a-z0-9_]+)*\.(aero|arpa|biz|com|coop|edu|gov|info|int|mil|museum|name|net|org|pro|travel|mobi|[a-z][a-z])|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})?$/i);

    $('#form').submit(function(evt) {
      evt.preventDefault();
      $('#feedback').html('');

      var password = $('#create-password').val();
      var email = $('#create-email').val().trim();
      email = email ? email.trim() : null;

      if (!email && !password) {
        $('#feedback').html('Input credentials.').attr('class', 'error');
        return;
      } else if (!email) {
        $('#feedback').html('Input email').attr('class', 'error');
        return;
      } else if (!EMAIL_REGEX.test(email)) {
        $('#feedback').html('Invalid email').attr('class', 'error');
        return;
      } else if (!password) {
        $('#feedback').html('Input password').attr('class', 'error');
        return;
      }

      $.ajax({
        type: "POST",
        url: '/create',
        data: {
          email: email,
          password: password,
          chapterID: $('#select-box').val()
        },
        success: function() {
          $('#feedback').html('User created.').attr('class', 'success');
        },
        error: function() {
          $('#feedback').html('Could not create user.').attr('class', 'error');
          console.log('error.');
        }
      });
    });