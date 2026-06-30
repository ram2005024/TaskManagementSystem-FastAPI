const SocialLogin = () => (
  <div className="mt-5 space-y-3">
    <button className="w-full flex items-center gap-2 justify-center bg-white border py-2.5 rounded-full text-gray-800">
      <img
        className="w-4 h-4"
        src="https://raw.githubusercontent.com/prebuiltui/prebuiltui/main/assets/login/googleFavicon.png"
        alt="googleLogo"
      />
      Log in with Google
    </button>

    <button className="w-full flex items-center gap-2 justify-center bg-white border py-2.5 rounded-full text-gray-800">
      <img
        className="w-4 h-4"
        src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
        alt="githubLogo"
      />
      Log in with GitHub
    </button>

    <button className="w-full flex items-center gap-2 justify-center bg-blue-600 py-2.5 rounded-full text-white">
      <img
        className="w-4 h-4"
        src="https://www.facebook.com/images/fb_icon_325x325.png"
        alt="facebookLogo"
      />
      Log in with Facebook
    </button>
  </div>
);
export default SocialLogin;
