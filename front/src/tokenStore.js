let accessToken = null;

export const tokenStore = {
  get: () => accessToken,
  set: (t) => { accessToken = t; },
  clear: () => { accessToken = null; },
  has: () => Boolean(accessToken),
};
