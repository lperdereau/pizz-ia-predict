apiVersion: apps/v1
kind: Deployment
metadata:
  name: pizz-ia-predict
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pizz-ia-predict
  template:
    metadata:
      labels:
        app: pizz-ia-predict
    spec:
      containers:
      - name: pizz-ia-predict
        image: docker.pkg.github.com/lperdereau/pizz-ia-predict/app:$GITHUB_SHA
        imagePullPolicy: Always

        ports:
        - name: http
          containerPort: 5000

        readinessProbe:
          tcpSocket:
            port: http
          initialDelaySeconds: 5
          periodSeconds: 10

      imagePullSecrets:
      - name: git-registry.pw.fr
