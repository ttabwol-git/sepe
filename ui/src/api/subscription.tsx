const apiUrl = process.env.NEXT_PUBLIC_API_URL?.toString() ?? "";

interface queueSubscriptionResponse {
  detail: string;
  validation_token: string;
}

interface genericResponse {
  detail: string;
}

export const queueSubscription = async (postalCode: string, email: string) => {
  const url = new URL(apiUrl);
  url.pathname = "/subscription/queue";
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      postal_code: postalCode,
      user_email: email,
    }),
  });
  const data: queueSubscriptionResponse = await response.json();
  return data;
};

export const validateSubscription = async (token: string) => {
  const url = new URL(apiUrl);
  url.pathname = "/subscription/validate";
  url.searchParams.append("token", token);
  const response = await fetch(url);
  const data: genericResponse = await response.json();
  return data;
};

export const removeSubscription = async (token: string) => {
  const url = new URL(apiUrl);
  url.pathname = "/subscription/remove";
  url.searchParams.append("token", token);
  const response = await fetch(url);
  const data: genericResponse = await response.json();
  return data;
};
