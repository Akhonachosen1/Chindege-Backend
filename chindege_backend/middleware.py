from django.http import JsonResponse, HttpResponse

class ResponseTypeLoggerMiddleware:
    """Logs response types and guards against non-HTTP responses."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Debug log
        print(f"[DEBUG] Response type: {type(response)}")

        # Catch any accidental raw dict responses
        if isinstance(response, dict):
            print("[ERROR] Middleware intercepted raw dict. Wrapping in JsonResponse.")
            return JsonResponse(response)

        if not isinstance(response, HttpResponse):
            print("[ERROR] Unexpected response type in middleware.")
            return JsonResponse({"error": "Unexpected response type from view."}, status=500)

        return response
          2avkja-codex/create-tests-for-generate_crash_point,-start_new_round,-and main
