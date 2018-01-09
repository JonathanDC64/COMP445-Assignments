package ca.concordia.request;

public class Response {
	private String header;
	private String body;

	public Response(String header, String body) {
		super();
		this.header = header;
		this.body = body;
	}

	public String getHeader() {
		return header;
	}

	public void setHeader(String header) {
		this.header = header;
	}

	public String getBody() {
		return body;
	}

	public void setBody(String body) {
		this.body = body;
	}

}
