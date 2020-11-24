import datetime
from flask import *
from config import *

error_app = None

def start_error_app():
    global error_app
    error_app = Flask(__name__)

    @error_app.context_processor
    def inject_year_to_all_templates():
        return dict(year=get_year())

    @error_app.route("{0}/".format(HOST_PREFIX))
    def home():
        return load_error_page(502, 'Bad Gateway', 'Due to a power outage and the building\'s COVID-related closure, '
                                                   'the AHS heatmap is unable to access sensor data and will remain '
                                                   'down until further notice.')

    @error_app.route("{0}/about".format(HOST_PREFIX))
    def about():
        return redirect("{0}/".format(HOST_PREFIX))

    @error_app.route("{0}/ahs/<floor>".format(HOST_PREFIX))
    def load_svg(floor):
        return redirect("{0}/".format(HOST_PREFIX))

    @error_app.errorhandler(404)
    def error_404(e):
        return load_error_page(404, 'Page Not Found', 'The page you are looking for might have been removed, had its ' +
                               'name changed, or be temporarily unavailable.')

    @error_app.errorhandler(403)
    def error_403(e):
        return load_error_page(403, 'Forbidden', 'You don\'t have permission to access this page on this server')

    @error_app.errorhandler(500)
    def error_500(e):
        return load_error_page(500, 'Internal Server Error', Markup('The server encountered an internal error or ' +
                                                                    'misconfiguration and was unable to complete your request. <br><br>' +
                                                                    'Please contact Daniel Ivanovich (<a href="mailto:dan@ivanovi.ch">dan@ivanovi.ch</a>) ' +
                                                                    'to make this issue known.'))

    def load_error_page(code, tagline, details):
        return render_template('down_error.html', code=str(code), tagline=tagline, details=details), code

    # register new; the same view function is used
    error_app.add_url_rule(
        error_app.static_url_path + '/<path:filename>',
        endpoint='static', view_func=error_app.send_static_file)


def get_year():
    return datetime.datetime.now().year


start_error_app()

if __name__ == '__main__':
    error_app.run()
