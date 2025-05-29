from flask import make_response, render_template

from page_analyzer.entities.schemas.url_schema import (
    CheckSchema,
    UrlSchema,
    UrlWithLastCheckSchema,
)


class UrlPresentation:
    @staticmethod
    def render_index(template_name: str):
        return render_template(template_name)

    @staticmethod
    def render_add_data_for_url_page(
        template_name: str, list_urls: list, code: int
    ):
        html = render_template(
            template_name_or_list=template_name, list_urls=list_urls
        )
        return make_response(html, code)

    @staticmethod
    def render_data_for_url(
        template_name: str,
        url_data: UrlSchema | None = None,
        checks_data: list[CheckSchema] | None = None,
    ):
        return render_template(
            template_name_or_list=template_name,
            url_data=url_data,
            checks_data=checks_data,
        )

    @staticmethod
    def render_data_for_all_url(urls: list[UrlWithLastCheckSchema]):
        return render_template(
            template_name_or_list="show_all_urls.html", urls=urls
        )
