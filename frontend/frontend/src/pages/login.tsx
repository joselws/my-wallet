export default function Login() {
  return (
    <>
      <div className="min-h-full flex flex-col justify-center py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <img
            className="mx-auto h-12 w-auto"
            src="../../wallet.png"
            alt="Workflow"
          />
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            My Wallet
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            <a
              href="#"
              className="font-medium text-yellow-600 hover:text-yellow-500"
            >
              Sign in!
            </a>
          </p>
        </div>

        <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
          <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
            <form className="space-y-6" action="#" method="POST">
              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700"
                >
                  Email address
                </label>
                <div className="mt-1">
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm"
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium text-gray-700"
                >
                  Password
                </label>
                <div className="mt-1">
                  <input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-yellow-500 focus:border-yellow-500 sm:text-sm"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="remember-me"
                    name="remember-me"
                    type="checkbox"
                    className="h-4 w-4 text-yellow-600 focus:ring-yellow-500 border-gray-300 rounded"
                  />
                  <label
                    htmlFor="remember-me"
                    className="ml-2 block text-sm text-gray-900"
                  >
                    Remember me
                  </label>
                </div>

                <div className="text-sm">
                  <a
                    href="#"
                    className="font-medium text-yellow-600 hover:text-yellow-500"
                  >
                    Forgot your password?
                  </a>
                </div>
              </div>

              <div>
                <button
                  type="submit"
                  className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500"
                >
                  Sign in
                </button>
              </div>
            </form>

            <div className="mt-6">
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">
                    Or continue with
                  </span>
                </div>
              </div>

              <div className="mt-6 grid grid-cols-1 gap-3">
                <div>
                  <a
                    href="#"
                    className=" w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                  >
                    <span className="sr-only">Sign in with Facebook</span>

                    <svg
                      className="w-5 h-5"
                      aria-hidden="true"
                      fill="currentColor"
                      id="Capa_1"
                      enable-background="new 0 0 512 512"
                      height="512"
                      viewBox="0 0 512 512"
                      width="512"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <g>
                        <path
                          d="m420.7 450.7c-44.4 37.5-101.999 61.3-164.7 61.3-93.3 0-175.201-51.4-219.6-126.4l16.622-76.622 73.678-13.678c17.1 55.199 68.699 95.7 129.3 95.7 29.399 0 56.7-9.3 79.2-25.8l70.8 10.8z"
                          fill="#59c36a"
                        />
                        <path
                          d="m420.7 450.7-14.7-74.7-70.8-10.8c-22.5 16.5-49.801 25.8-79.2 25.8v121c62.701 0 120.3-23.8 164.7-61.3z"
                          fill="#00a66c"
                        />
                        <g id="Connected_Home_1_">
                          <g>
                            <g>
                              <g>
                                <path
                                  d="m121 256c0 13.799 2.1 26.999 5.7 39.3l-90.3 90.3c-22.5-37.8-36.4-82.201-36.4-129.6 0-47.401 13.9-91.8 36.4-129.6l72.473 12.473 17.827 77.827c-3.6 12.299-5.7 25.499-5.7 39.3z"
                                  fill="#ffda2d"
                                />
                              </g>
                            </g>
                          </g>
                        </g>
                        <path
                          d="m512 256c0 77.999-36.099 147.9-91.3 194.7l-85.5-85.5c17.399-12.601 32.1-29.401 41.7-49.2h-120.9c-8.401 0-15-6.601-15-15v-90c0-8.401 6.599-15 15-15h236.8c7.2 0 13.5 5.099 14.7 12.299 3 15.601 4.5 31.8 4.5 47.701z"
                          fill="#4086f4"
                        />
                        <path
                          d="m376.901 316c-9.6 19.799-24.302 36.599-41.749.2l85.499 85.5c55.201-46.8 91.3-116.7 91.3-194.7 0-15.901-1.5-32.1-4.501-47.701-1.199-7.2-7.5-12.299-14.7-12.299h-236.799v120z"
                          fill="#4175df"
                        />
                        <path
                          d="m424.9 71.499c.3 4.2-1.5 8.101-4.2 11.1l-64.2 63.9c-5.099 5.4-13.499 6-19.499 1.5-23.702-17.699-51.602-26.999-81.001-26.999-60.601 0-112.2 40.499-129.3 95.7l-90.3-90.3c44.399-75 126.3-126.4 219.6-126.4 59.7 0 117.9 22 163.5 60.399 3.3 2.701 5.1 6.9 5.4 11.1z"
                          fill="#ff641a"
                        />
                        <path
                          d="m337 147.999c6 4.501 14.399 3.9 19.499-1.5l64.2-63.9c2.701-2.999 4.501-6.899 4.2-11.1s-2.1-8.399-5.4-11.1c-45.599-38.399-103.799-60.399-163.499-60.399v121c29.399 0 57.299 9.3 81 26.999z"
                          fill="#f03800"
                        />
                      </g>
                    </svg>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
