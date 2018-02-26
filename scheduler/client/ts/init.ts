
// Exported bootstrap function for initializing the app.
export function init() {
  setupCsrf();
}

// Setup to comply with the django server's CSRF protection scheme.
function setupCsrf() {
  const csrftoken = ($("[name=csrfmiddlewaretoken]").val() as string);
  // these HTTP methods do not require CSRF protection
  function csrfSafeMethod(method: string) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // Only add the CSRF token to certain requests to the current domain to avoid the token leaking out.
  $.ajaxSetup({
    beforeSend: (xhr: JQuery.jqXHR, settings: JQuery.PlainObject) => {
      if (!csrfSafeMethod(settings.type) && !settings.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });
}
