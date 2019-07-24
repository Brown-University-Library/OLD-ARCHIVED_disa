class DISASource {

  constructor(baseURL, endpoints, csrfToken) {
    this._base = baseURL;
    this._app = {};

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("Access-Control-Allow-Origin", "http://0.0.0.0:5000");

        if (RegExp('^(POST|PUT|PATCH|DELETE)$').test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
      }
    });
  }

  registerApp( app ) {
    this._app = app;
  }

  request( endpoint, method, callback, payload ) {
    let settings = {
      type: method,
      dataType: "json",      
      url: endpoint,
      context: this,
      success: function( data ) {
        this._app[callback]( data );
      }
    };

    if (method === 'POST' || method === 'PUT') {
      settings.contentType = "application/json";
      settings.data = JSON.stringify(payload);
    }
    $.ajax(settings);
  }


  deleteReference(citeId, refId) {
    var endpoint = this._base + `data/citation/${citeId}/references/${refId}`;
    this.request(endpoint, 'DELETE', 'referenceDeleted');
  }


  createCitation(data) {
    var endpoint = this._base + `data/citations/`;
    this.request(endpoint, 'POST', 'citationSaved', data);
  }

  updateCitation(citeId, data) {
    var endpoint = this._base + `data/citations/${citeId}`;
    this.request(endpoint, 'PUT', 'citationSaved', data);
  }
}