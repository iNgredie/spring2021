import logging
from drfpasswordless.settings import api_settings
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.tokens import AccessToken
from .smsc_api import SMSC, SMSCException


logger = logging.getLogger(__name__)


def smsc_send_sms_with_callback_token(user, mobile_token, **kwargs):

    if api_settings.PASSWORDLESS_TEST_SUPPRESSION is True:
        # we assume success to prevent spamming SMS during testing.

        # even if you have suppression on– you must provide a number if you have mobile selected.
        if api_settings.PASSWORDLESS_MOBILE_NOREPLY_NUMBER is None:
            return False

        return True

    base_string = kwargs.get('mobile_message', api_settings.PASSWORDLESS_MOBILE_MESSAGE)

    try:
        if api_settings.PASSWORDLESS_MOBILE_NOREPLY_NUMBER:
            # We need a sending number to send properly

            smsc = SMSC()

            to_number = getattr(user, api_settings.PASSWORDLESS_USER_MOBILE_FIELD_NAME)
            if to_number.__class__.__name__ == 'PhoneNumber':
                to_number = to_number.__str__()

            answer = smsc.send_sms(
                phones=to_number,
                message=base_string % mobile_token.key,
                sender=api_settings.PASSWORDLESS_MOBILE_NOREPLY_NUMBER
            )

            if len(answer) == 2:
                raise SMSCException(*answer)

            return True
        else:
            logger.debug("Failed to send token sms. Missing PASSWORDLESS_MOBILE_NOREPLY_NUMBER.")
            return False
    except SMSCException:
        logger.debug("SMSC error")
    except Exception as e:
        logger.debug("Failed to send token SMS to user: {}. "
                     "Possibly no mobile number on user object or SMSC isn't set up yet. "
                     "Number entered was {}".format(user.id,
                                                    getattr(user, api_settings.PASSWORDLESS_USER_MOBILE_FIELD_NAME)))
        logger.debug(e)
        return False


def get_token_for_user(user):
    return (AccessToken.for_user(user), None)


class OptionalSlashRouter(DefaultRouter):
    """
    Роутер с опциональным заключительным слэшем
    """

    def __init__(self):
        super().__init__()
        self.trailing_slash = '/?'
