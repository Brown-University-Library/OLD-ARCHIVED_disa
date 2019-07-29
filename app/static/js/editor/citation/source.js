class DISASource {

  constructor($endpoints, $csrfToken) {
    this._app = {};
    this.endpoints = this.getEndpoints($endpoints);
    this._csrf = $csrfToken.attr('data-csrf');

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("Access-Control-Allow-Origin", "http://0.0.0.0:5000");

        if (RegExp('^(POST|PUT|PATCH|DELETE)$').test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", this._csrf);
        }
      }
    });
  }

  registerApp( app ) {
    this._app = app;
  }

  getEndpoints( $endpoints ) {
    let endpoint_map = {};

    $endpoints.find('.endpoint').each(function() {
      endpoint_map[$(this).attr('data-name')] = $(this).attr('data-url');
    });

    return endpoint_map;
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


  deleteReference(refId) {
    var endpoint = this.endpoints.deleteReference + refId;
    this.request(endpoint, 'DELETE', 'referenceDeleted');
  }


  createCitation(data) {
    var endpoint = this.endpoints.createCitation;
    this.request(endpoint, 'POST', 'citationSaved', data);
  }

  updateCitation(data) {
    var endpoint = this.endpoints.updateCitation;
    this.request(endpoint, 'PUT', 'citationSaved', data);
  }
}