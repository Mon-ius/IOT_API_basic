export CF_Key={{KEY}}
export CF_Email={{EMAIL}}

/root/.acme.sh/acme.sh --issue -d "*.{{DOMAIN}}" -d "{{DOMAIN}}" --dns dns_cf \
--cert-file /etc/nginx/certs/site.crt \
--key-file /etc/nginx/certs/site.key \
--fullchain-file /etc/nginx/certs/fullchain.crt \
--ca-file /etc/nginx/certs/ca.crt 