class Flow {

  constructor(){}

  setApp(obj) {
    this._app = obj;
  }

  getTemplates($elem) {
    let template_map = {};
    let $templates = $elem.find('template');
    $templates.each(function() {
      let $tmpl = $( $(this).prop('content') ).children().first();
      $tmpl.detach();
      template_map[$tmpl.attr('id')] = $tmpl;
      $tmpl.removeAttr('id');
      $(this).remove();
    });
    return template_map;
  }
}

class Config {

  constructor($elem) {
    this._$root = $elem;
    this._data = JSON.parse(
      this._$root.find('#config_data_json').attr('data-json'));
  }

  get(attr) {
    return this._data[attr];
  }
}