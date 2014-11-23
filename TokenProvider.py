import vipaccess

class TokenProvider():
      def set_token(token, request, *args, **kwargs):
          # generate_a_TOTP_token
          #tok = Token(**token)
          #tok.user_id = request.user_id
          #tok.client_id = request.client.client_id
          #db.session.add(tok)
          #db.session.commit()
          token = getOTT() 

      def get_token(access_token=None):
          #if access_token:
          #   return Token.query.filter_by(access_token=access_token).first()
          return None
          
      def getOTT():
          request = vipaccess.generate_request()
          response = requests.post(PROVISIONING_URL, data=request)
          otp_token = vipaccess.get_token_from_response(response.content)
          otp_secret = vipaccess.decrypt_key(otp_token['iv'], otp_token['cipher'])
          if not vipaccess.check_token(otp_token['id'], otp_secret):
            sys.stderr.write("Something went wrong--the token is invalid.\n")
            sys.exit(1)
          otp = totp(binascii.b2a_hex(otp_secret))
          return otp
