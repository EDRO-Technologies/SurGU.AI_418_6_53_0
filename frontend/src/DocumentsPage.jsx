import React, { useState, useEffect, useRef } from "react";
import { useNavigate } from 'react-router-dom'
import { Button, Card, CardBody, Input } from "@heroui/react";
import { FileText, ArrowLeft, Plus, LogOut, ChevronLeft, ChevronRight, X, Download } from "lucide-react";

const DocumentsPage = () => {
  const navigate = useNavigate()
  const [documents, setDocuments] = useState([]);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const [description, setDescription] = useState("");
  const [dialogMode, setDialogMode] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadDescription, setUploadDescription] = useState("");
  const [showUploadDialog, setShowUploadDialog] = useState(false);
  const fileInputRef = useRef(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const itemsPerPage = 6;

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/v1/document?skip=0&limit=100', {
        method: 'GET',
        credentials: 'include',
      });
      
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      } else if (response.status === 401) {
        navigate('/');
      }
    } catch (error) {
      console.error('Error fetching documents:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const totalPages = Math.ceil(documents.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentDocuments = documents.slice(startIndex, endIndex);

  const openDialog = (doc) => {
    setSelectedDoc(doc);
    setDescription(doc.description || "");
    setDialogMode('view');
  };

  const closeDialog = () => {
    setSelectedDoc(null);
    setDescription("");
    setDialogMode(null);
  };

  const switchToEdit = () => {
    setDialogMode('edit');
  };

  const switchToDelete = () => {
    setDialogMode('delete');
  };

  const saveDescription = () => {
    if (selectedDoc) {
      setDocuments(docs =>
        docs.map(doc =>
          doc.id === selectedDoc.id ? { ...doc, description } : doc
        )
      );
      setSelectedDoc({ ...selectedDoc, description });
      setDialogMode('view');
    }
  };

  const confirmDelete = async () => {
    if (selectedDoc) {
      try {
        const response = await fetch(`/api/v1/document/${selectedDoc.id}`, {
          method: 'DELETE',
          credentials: 'include',
        });
        
        if (response.status === 204) {
          setDocuments(docs => docs.filter(doc => doc.id !== selectedDoc.id));
          if (currentDocuments.length === 1 && currentPage > 1) {
            setCurrentPage(currentPage - 1);
          }
        }
      } catch (error) {
        console.error('Error deleting document:', error);
      }
    }
    closeDialog();
  };

  const openUploadDialog = () => {
    setShowUploadDialog(true);
    setUploadDescription("");
    setSelectedFile(null);
  };

  const closeUploadDialog = () => {
    setShowUploadDialog(false);
    setUploadDescription("");
    setSelectedFile(null);
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const uploadFile = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);
    if (uploadDescription) {
      formData.append('description', uploadDescription);
    }

    try {
      const response = await fetch('/api/v1/document', {
        method: 'POST',
        credentials: 'include',
        body: formData
      });

      if (response.status === 201) {
        const newDoc = await response.json();
        setDocuments([...documents, newDoc]);
        setCurrentPage(Math.ceil((documents.length + 1) / itemsPerPage));
        closeUploadDialog();
      }
    } catch (error) {
      console.error('Error uploading document:', error);
    }
  };

  const downloadDocument = async (docId, filename) => {
    try {
      const response = await fetch(`/api/v1/document/${docId}/download`, {
        method: 'GET',
        credentials: 'include',
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Error downloading document:', error);
    }
  };

  const logout = async () => {
    try {
      await fetch('/api/v1/auth/logout', {
        method: 'POST',
        credentials: 'include',
      });
    } catch (error) {
      console.error('Error during logout:', error);
    }
    navigate('/');
  };

  const changePage = (page) => {
    setCurrentPage(page);
  };

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <Button
          isIconOnly
          className="bg-transparent hover:bg-gray-100 rounded-lg transition-colors"
          onClick={() => navigate('/dashboard')}
        >
          <ArrowLeft size={20} className="text-black" />
        </Button>
        <h1 style={styles.title}>Мои документы</h1>
        <Button
          isIconOnly
          className="bg-transparent hover:bg-gray-200 rounded-full transition-colors"
          onClick={logout}
        >
          <LogOut size={20} className="text-black" />
        </Button>
      </div>

      <div style={styles.addButtonContainer}>
        <Button
          onClick={openUploadDialog}
          className="bg-black text-white font-semibold uppercase rounded-lg px-6 flex items-center gap-2"
        >
          <Plus size={18} />
          Добавить документ
        </Button>
      </div>

      <div style={styles.gridContainer}>
        {isLoading ? (
          <p style={styles.emptyText}>Загрузка...</p>
        ) : currentDocuments.length === 0 ? (
          <p style={styles.emptyText}>Документы отсутствуют</p>
        ) : (
          currentDocuments.map(doc => (
            <Card key={doc.id} className="border border-gray-200 shadow-sm hover:shadow-md transition-shadow" style={styles.docCard}>
              <CardBody className="gap-4 p-6">
                <div style={styles.fileHeader}>
                  <FileText size={32} className="text-gray-600" />
                  <p style={styles.fileName}>{doc.filename}</p>
                </div>

                <p style={styles.description}>
                  {doc.description || "Описание отсутствует"}
                </p>

                <div style={styles.cardButtons}>  
                  <Button
                    onClick={() => openDialog(doc)}
                    className="flex-1 bg-white text-black border-2 border-black font-semibold rounded-lg py-2 hover:bg-gray-100 transition-colors"
                  >
                    Подробнее
                  </Button>
                </div>
              </CardBody>
            </Card>
          ))
        )}
      </div>

      {documents.length > itemsPerPage && (
        <div style={styles.paginationContainer}>
          <Button
            isIconOnly
            className="bg-transparent border border-gray-300 text-black rounded-lg hover:bg-gray-100"
            onClick={() => changePage(currentPage - 1)}
            disabled={currentPage === 1}
          >
            <ChevronLeft size={20} />
          </Button>

          <div style={styles.paginationInfo}>
            <select 
              value={currentPage}
              onChange={(e) => changePage(Number(e.target.value))}
              style={styles.pageSelect}
            >
              {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                <option key={page} value={page}>
                  Страница {page} из {totalPages}
                </option>
              ))}
            </select>
          </div>

          <Button
            isIconOnly
            className="bg-transparent border border-gray-300 text-black rounded-lg hover:bg-gray-100"
            onClick={() => changePage(currentPage + 1)}
            disabled={currentPage === totalPages}
          >
            <ChevronRight size={20} />
          </Button>
        </div>
      )}

      {showUploadDialog && (
        <div style={styles.overlay} onClick={closeUploadDialog}>
          <div style={styles.dialog} onClick={(e) => e.stopPropagation()}>
            <button style={styles.closeBtn} onClick={closeUploadDialog}>
              <X size={24} />
            </button>

            <h2 style={styles.dialogTitle}>Загрузить документ</h2>

            <div style={styles.dialogContent}>
              <div style={styles.uploadArea}>
                <input
                  ref={fileInputRef}
                  type="file"
                  onChange={handleFileSelect}
                  style={styles.fileInput}
                />
                {selectedFile && (
                  <p style={styles.selectedFileName}>{selectedFile.name}</p>
                )}
              </div>

              <div style={styles.inputGroup}>
                <label style={styles.label}>Описание (необязательно):</label>
                <textarea
                  value={uploadDescription}
                  onChange={(e) => setUploadDescription(e.target.value)}
                  placeholder="Введите описание документа"
                  style={styles.textarea}
                  rows={3}
                />
              </div>
            </div>

            <div style={styles.dialogButtons}>
              <Button
                onClick={closeUploadDialog}
                className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-gray-100 transition-colors"
              >
                Отмена
              </Button>
              <Button
                onClick={uploadFile}
                disabled={!selectedFile}
                className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-green-300 transition-colors disabled:opacity-50"
              >
                Загрузить
              </Button>
            </div>
          </div>
        </div>
      )}

      {dialogMode && (
        <div style={styles.overlay} onClick={closeDialog}>
          <div style={styles.dialog} onClick={(e) => e.stopPropagation()}>
            <button style={styles.closeBtn} onClick={closeDialog}>
              <X size={24} />
            </button>

            <h2 style={styles.dialogTitle}>
              {dialogMode === 'delete' 
                ? 'Удалить документ?' 
                : dialogMode === 'edit'
                ? 'Редактировать описание'
                : 'Детали документа'
              }
            </h2>

            <div style={styles.dialogContent}>
              {dialogMode === 'delete' && (
                <div>
                  <p style={styles.text}>
                    Вы уверены, что хотите удалить <strong>{selectedDoc?.filename}</strong>?
                  </p>
                  <p style={styles.warning}>Это действие невозможно отменить.</p>
                </div>
              )}

              {dialogMode === 'edit' && (
                <div>
                  <label style={styles.label}>Файл:</label>
                  <p style={styles.fileName}>{selectedDoc?.filename}</p>
                  <Input
                    label="Описание"
                    placeholder="Введите описание документа"
                    value={description}
                    onValueChange={setDescription}
                    fullWidth
                    classNames={{
                      input: "bg-transparent text-black",
                      label: "text-black font-semibold text-sm",
                      inputWrapper: "bg-gray-100 border border-gray-300 rounded-lg",
                    }}
                  />
                </div>
              )}

              {dialogMode === 'view' && (
                <div>
                  <div style={styles.infoBlock}>
                    <label style={styles.label}>Название файла:</label>
                    <p style={styles.infoValue}>{selectedDoc?.filename}</p>
                  </div>
                  <div style={styles.infoBlock}>
                    <label style={styles.label}>Размер:</label>
                    <p style={styles.infoValue}>
                      {selectedDoc?.size ? `${(selectedDoc.size / 1024 / 1024).toFixed(2)} MB` : 'Неизвестно'}
                    </p>
                  </div>
                  <div style={styles.infoBlock}>
                    <label style={styles.label}>Дата загрузки:</label>
                    <p style={styles.infoValue}>
                      {selectedDoc?.upload_date ? new Date(selectedDoc.upload_date).toLocaleString('ru-RU') : 'Неизвестно'}
                    </p>
                  </div>
                  <div style={styles.infoBlock}>
                    <label style={styles.label}>Описание:</label>
                    <p style={styles.infoValue}>
                      {selectedDoc?.description || "Описание отсутствует"}
                    </p>
                  </div>
                </div>
              )}
            </div>

            <div style={styles.dialogButtons}>
              {dialogMode === 'view' && (
                <>
                  <Button
                    onClick={switchToDelete}
                    className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-red-300 transition-colors"
                  >
                    Удалить
                  </Button>
                  <Button
                    onClick={() => downloadDocument(selectedDoc.id, selectedDoc.filename)}
                    className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-blue-300 transition-colors"
                  >
                    Скачать
                  </Button>
                  <Button
                    onClick={closeDialog}
                    className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-gray-100 transition-colors"
                  >
                    Закрыть
                  </Button>
                </>
              )}

              {dialogMode === 'edit' && (
                <>
                  <Button
                    onClick={() => setDialogMode('view')}
                    className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-gray-100 transition-colors"
                  >
                    Отмена
                  </Button>
                  <Button
                    onClick={saveDescription}
                    className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-green-300 transition-colors"
                  >
                    Сохранить
                  </Button>
                </>
              )}

              {dialogMode === 'delete' && (
                <>
                  <Button
                    onClick={() => setDialogMode('view')}
                    className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-gray-100 transition-colors"
                  >
                    Отмена
                  </Button>
                  <Button
                    onClick={confirmDelete}
                    className="bg-transparent text-black border-2 border-black font-semibold rounded-lg flex-1 hover:bg-red-300 transition-colors"
                  >
                    Удалить
                  </Button>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const styles = {
  page: {
    minHeight: "100vh",
    background: "#ffffff",
    padding: "20px",
    fontFamily: "'Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', sans-serif",
    display: "flex",
    flexDirection: "column",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "40px",
    maxWidth: "1200px",
    margin: "0 auto 40px",
    width: "100%",
  },
  title: {
    fontSize: "28px",
    fontWeight: "700",
    color: "#000000",
    margin: 0,
  },
  addButtonContainer: {
    display: "flex",
    justifyContent: "center",
    marginBottom: "40px",
    maxWidth: "1200px",
    margin: "0 auto 40px",
    width: "100%",
  },
  gridContainer: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
    gap: "24px",
    maxWidth: "1200px",
    margin: "0 auto 40px",
    width: "100%",
    flex: 1,
    alignItems: "start",
  },
  docCard: {
    borderRadius: "12px",
    transition: "all 0.3s ease",
    height: "fit-content",
  },
  fileHeader: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
  },
  fileName: {
    fontSize: "16px",
    fontWeight: "600",
    color: "#000000",
    margin: 0,
    wordBreak: "break-word",
  },
  description: {
    fontSize: "13px",
    color: "#666666",
    margin: 0,
    lineHeight: "1.5",
    wordBreak: "break-word",
  },
  cardButtons: {
    display: "flex",
    gap: "8px",
    marginTop: "auto",
  },
  emptyText: {
    textAlign: "center",
    color: "#999999",
    fontSize: "16px",
    gridColumn: "1 / -1",
  },
  paginationContainer: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "16px",
    marginTop: "40px",
    maxWidth: "1200px",
    margin: "40px auto 0",
    width: "100%",
  },
  paginationInfo: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
  },
  pageSelect: {
    padding: "8px 12px",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    fontSize: "14px",
    fontFamily: "inherit",
    cursor: "pointer",
    background: "#ffffff",
  },
  overlay: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: "rgba(0, 0, 0, 0.5)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 9999,
  },
  dialog: {
    background: "#ffffff",
    borderRadius: "12px",
    boxShadow: "0 20px 60px rgba(0, 0, 0, 0.3)",
    width: "90%",
    maxWidth: "500px",
    padding: "0",
    position: "relative",
  },
  closeBtn: {
    position: "absolute",
    top: "16px",
    right: "16px",
    background: "none",
    border: "none",
    cursor: "pointer",
    padding: "8px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    color: "#000000",
    zIndex: 10000,
  },
  dialogTitle: {
    fontSize: "20px",
    fontWeight: "700",
    color: "#000000",
    padding: "24px 24px 0",
    margin: 0,
    borderBottom: "1px solid #e5e5e5",
    paddingBottom: "16px",
  },
  dialogContent: {
    padding: "24px",
  },
  text: {
    fontSize: "14px",
    color: "#333333",
    margin: "0 0 12px 0",
  },
  warning: {
    fontSize: "12px",
    color: "#ff6b6b",
    margin: "0",
    fontWeight: "500",
  },
  label: {
    fontSize: "13px",
    fontWeight: "600",
    color: "#000000",
    margin: "0 0 8px 0",
    display: "block",
  },
  infoBlock: {
    marginBottom: "16px",
  },
  infoValue: {
    fontSize: "14px",
    color: "#333333",
    padding: "8px 12px",
    background: "#f8f8f8",
    borderRadius: "6px",
    margin: "0",
  },
  dialogButtons: {
    padding: "16px 24px",
    borderTop: "1px solid #e5e5e5",
    display: "flex",
    gap: "8px",
    flexWrap: "wrap",
  },
  uploadArea: {
    marginBottom: "20px",
  },
  fileInput: {
    width: "100%",
    padding: "12px",
    border: "2px dashed #e0e0e0",
    borderRadius: "8px",
    cursor: "pointer",
  },
  selectedFileName: {
    marginTop: "8px",
    fontSize: "14px",
    color: "#666666",
  },
  inputGroup: {
    marginBottom: "16px",
  },
  textarea: {
    width: "100%",
    padding: "8px 12px",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    fontSize: "14px",
    fontFamily: "inherit",
    resize: "vertical",
  },
};

export default DocumentsPage;