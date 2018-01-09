package ca.concordia.get;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.stream.Collectors;

public class Get {
	private static String header(String uri, String host) {
		return String.format(
				"GET %s HTTP/1.0\r\n" + 
				"Host: %s\r\n" + 
				"\r\n"

				, uri, host);
	}

	private static void sendRequest(String header, BufferedWriter out) throws IOException {
		out.write(header);
		out.flush();
	}

	private static String getReponse(BufferedReader in) throws IOException {
		return in.lines().collect(Collectors.joining("\n"));
	}

	public static String request(String uri, String host) throws IOException {
		return request(uri, host, 80);
	}

	public static String request(String uri, String host, int port) throws IOException {
		try (Socket socket = new Socket(host,port)) {
			socket.setTcpNoDelay(true);
			BufferedWriter out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream(), "UTF8"));
			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			sendRequest(header(uri, host), out);
			String response = getReponse(in);;
			in.close();
			out.close();
			return response;
		}
	}
	
	public static void main(String[] args) {
		try {
			System.out.println(request("/ip", "httpbin.org"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
