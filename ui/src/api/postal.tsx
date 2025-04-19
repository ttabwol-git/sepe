const apiUrl = process.env.NEXT_PUBLIC_API_URL?.toString() || "";

export const fetchPostals = async () => {
  const url = new URL(apiUrl);
  url.pathname = "/postal";
  const response = await fetch(url);
  const data = await response.json();
  return data;
};
