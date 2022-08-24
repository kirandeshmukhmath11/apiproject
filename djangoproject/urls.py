"""LV_Develop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from django.conf.urls import url
from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static

#from kyc.apis.karza_pan_authentication.views_pan_authentication import PANAuthentication
#from kyc.apis.karza_pan_authentication_advanced.views_pan_authentication_advanced import PANAuthenticationAdvanced
from kyc.apis.karza_bank_verification.views_bank_verification import BankVerification
#from kyc.apis.karza_bank_verification_advanced.views_bank_verification_advanced import BankVerificationAdvanced
#from kyc.apis.karza_entity_pan_profile.views_entity_pan_profile import EntityPANProfile
#from kyc.apis.karza_entity_gst_search_basis_pan.views_entity_gst_search_basis_pan import EntityGSTSearchBasisPAN
#from kyc.apis.karza_entity_gst_authentication.views_entity_gst_authentication import EntityGSTAuthentication
#from kyc.apis.karza_pan_status_check.views_pan_status_check import PANStatusCheck
#from kyc.apis.karza_ckyc_download.views_ckyc_download import CkycDownload
#from kyc.apis.karza_ckyc_search.views_ckyc_search import CkycSearch
#from kyc.apis.karza_kyc_ocr.views_kyc_ocr import KycOcr

#from cadoc.apis.get_ca_doc.view_get_cadoc import GetCADocAPI
#from schemedoc.apis.get_scheme_doc.view_get_schemedoc import GetSchemeDocAPI
#from lettersandnotices.apis.get_letters_and_notices.view_get_lettersandnotices import GetLettersAndNoticesAPI

#from leegality.apis.initiate_eagreement.views_initiate_eagreement import InitiateEAgreement
#from leegality.apis.fetch_eagreement_details.views_fetch_eagreement_details import FetchEAgreementDetails
#from termsheets.apis.get_termsheets.view_get_termsheets import GetTermSheetsAPI
from utilities.healthcheck.views import HealthCheckView
 ############################### Swagger API #########################
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from utilities.loggers.papertrail.views_get_papertrail_logs import GetPapertrailLogs

schema_view = get_schema_view(
    openapi.Info(
        title="LV API Documentation",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="sureshv@wishworkssolutions.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^kyckra_pan_authentication/$', PANAuthentication.as_view(), name='kyckra_pan_authentication'),
    #url(r'^kyckra_pan_authentication_advanced/$', PANAuthenticationAdvanced.as_view(), name='kyckra_pan_authentication_advanced'),
    #url(r'^kyckra_pan_status_check/$', PANStatusCheck.as_view(), name='kyckra_pan_status_check'),
    re_path(r'^kyckra_bank_account_verification/$', BankVerification.as_view(), name='kyckra_bank_account_verification'),
    #url(r'^kyckra_bank_account_verification_advanced/$', BankVerificationAdvanced.as_view(),
    #    name='kyckra_bank_account_verification_advanced'),
    #url(r'^kyckra_entity_pan_profile/$', EntityPANProfile.as_view(), name='kyckra_entity_pan_profile'),
    #url(r'^kyckra_entity_gst_search_basis_pan/$', EntityGSTSearchBasisPAN.as_view(), name='kyckra_entity_gst_search_basis_pan'),
    #url(r'^kyckra_entity_gst_authentication/$', EntityGSTAuthentication.as_view(), name='kyckra_entity_gst_authentication'),

    #url(r'^kyckra_kyc_ocr/$', KycOcr.as_view(), name='kyckra_kyc_ocr'),
    #url(r'^kyckra_ckyc_download/$', CkycDownload.as_view(), name='ckyc_download'),
    #url(r'^kyckra_ckyc_search/$', CkycSearch.as_view(), name='ckyc_search'),

    #url(r'^cadoc_get_ca_doc/$', GetCADocAPI.as_view()),
    #url(r'^schemedoc_get_scheme_doc/$', GetSchemeDocAPI.as_view()),
    #url(r'^lettersandnotices_get_lettersandnotices/$', GetLettersAndNoticesAPI.as_view()),
    #url(r'^initiate_e_agreement/$', InitiateEAgreement.as_view()),
    #url(r'^fetch_e_agreement_details/$', FetchEAgreementDetails.as_view()),
    #url(r'^fetch_termsheets/$', GetTermSheetsAPI.as_view()),

    re_path(r'^get_papertrail_logs/$', GetPapertrailLogs.as_view()),
    re_path(r'^health_check/$', HealthCheckView.as_view()),

    ############################### Swagger API #########################
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
