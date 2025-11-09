import React, { useState } from "react";
import { useNavigate } from 'react-router-dom'
import { Input, Button, Card, CardBody } from "@heroui/react";


const LoginPage = () => {
  const navigate = useNavigate()
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          username,
          password
        })
      });

      if (response.status === 204) {
        navigate('/dashboard');
      } else {
        setError("Имя пользователя или пароль неверны");
      }
    } catch (error) {
      setError("Ошибка подключения к серверу");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center p-4" style={styles.container}>
      <div className="w-full max-w-md" style={styles.wrapper}>
        <div style={styles.header}>
          <h1 style={styles.logo}>Админ-Панель</h1>
        </div>

        <Card className="border border-gray-200 shadow-sm" style={styles.card}>
          <CardBody className="gap-6 p-8">
            {error && (
              <div style={styles.errorBox}>
                <p style={styles.errorText}>{error}</p>
              </div>
            )}
            <form onSubmit={handleSubmit} className="flex flex-col gap-6">
              {error && (
                <div style={styles.errorBox}>
                  <p style={styles.errorText}>{error}</p>
              </div>
              )}

              <div className="flex flex-col gap-2">
                <label htmlFor="username" className="text-xs font-semibold uppercase text-black">
                  Имя пользователя
                </label>
                <Input
                  id="username"
                  type="text"
                  placeholder="username"
                  value={username}
                  onValueChange={setUsername}
                  classNames={{
                    input: "bg-transparent text-black text-base h-8",
                    mainWrapper: "h-full",
                    inputWrapper: "bg-gray-100 border border-gray-300 rounded-lg h-9",
                  }}
                  required
                  disabled={isLoading}
                />
              </div>
                
              <div className="flex flex-col gap-2">
                <label htmlFor="password" className="text-xs font-semibold uppercase text-black">
                  Пароль
                </label>
                <Input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onValueChange={setPassword}
                  classNames={{
                    input: "bg-transparent text-black text-base h-8",
                    mainWrapper: "h-full",
                    inputWrapper: "bg-gray-100 border border-gray-300 rounded-lg h-9",
                  }}
                  required
                  disabled={isLoading}
                />
              </div>
                
              <Button
                type="submit"
                isLoading={isLoading}
                className="w-full bg-black text-white font-semibold uppercase tracking-wider rounded-lg py-2"
              >
                {isLoading ? "Вход..." : "Войти"}
              </Button>
            </form>
                
          </CardBody>
        </Card>

        <p className="text-center text-xs text-gray-500 mt-8">
          © 2025 MEGA PROJECT. Все права защищены.
        </p>
      </div>
    </div>
  );
};


const styles = {
  container: {
    fontFamily: "'Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', sans-serif",
  },
  wrapper: {
    maxWidth: "420px",
  },
  header: {
    marginBottom: "48px",
    textAlign: "center",
  },
  logo: {
    fontSize: "32px",
    fontWeight: "700",
    letterSpacing: "-1px",
    color: "#000000",
    margin: "0 0 12px 0",
  },
  card: {
    borderRadius: "12px",
  },
  errorBox: {
    background: "#fee",
    border: "1px solid #fcc",
    borderRadius: "8px",
    padding: "12px",
  },
  errorText: {
    color: "#c33",
    margin: 0,
    fontSize: "14px",
    fontWeight: "500",
  },
};


export default LoginPage;