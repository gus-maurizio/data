package com.example;

import javax.enterprise.context.ApplicationScoped;

import org.apache.camel.builder.RouteBuilder;


@ApplicationScoped
public class CamelRouteTimerHealthCheck extends RouteBuilder {
	@Override
    public void configure() throws Exception {
        from("timer://healthcheck?period={{camel.timer.healthcheck.period}}")
        .routeId("healthcheck")
        .streamCaching()
        .setBody(simple("Hello from timer at ${header.firedTime}"))
        .to("log:healthcheck?level=INFO&showAll=true")
		.to("bean:myNamedBean?method=hello")
        .to("log:beanlog?level=INFO&showAll=true");
    }
}