class OneTimePasswordAlgorithm:
      DIGITS_POWER = [1,10,100,1000,10000,100000,1000000,10000000,100000000]
      def generateTOTP(self, key, time, returnDigits, crypto):
         codeDigits = int(returnDigits)
         result = ''
         #Using the counter
         #First 8 bytes are for the movingFactor
         #Compliant with base RFC 4226 (HOTP)
         while (len(time) < 16):
             time = "0" + time
         #Get the HEX in a Byte[]
         msg = bytearray(time.decode("hex"))
         k = bytearray(key.decode("hex"))
         import hmac
         hash = bytearray(hmac.new(k,msg,crypto).hexdigest())
         #put selected bytes into result int
         offset = int(int(hash[len(hash) - 1]) & 0xf)
         binary =  ((hash[offset] & 0x7f) << 24)|((hash[offset + 1] & 0xff) << 16)|((hash[offset + 2] & 0xff) << 8)|(hash[offset + 3] & 0xff)
         otp = int(binary % self.DIGITS_POWER[codeDigits])
         result = str(otp)
         while (len(result) < codeDigits):
             result = "0" + result
         return result
                       
