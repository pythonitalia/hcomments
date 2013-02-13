# -*- coding: UTF-8 -*-
from django.conf import settings

# callable invocato per verificare se l'utente collegato alla richiesta può
# essere considerato un moderatore per il commento
MODERATOR_REQUEST = getattr(settings, 'HCOMMENTS_MODERATOR_REQUEST', lambda request, comment: request.user.is_superuser)

# callable per identificare i proprietari di un thread di commenti, deve
# ritorna None o una lista di user
THREAD_OWNERS = getattr(settings, 'HCOMMENTS_THREAD_OWNERS', lambda o: None)

# callable per decidere se includere o meno un captcha nella form di commento;
# di default non viene incluso mai.
RECAPTCHA = getattr(settings, 'HCOMMENTS_RECAPTCHA', lambda request: False)
