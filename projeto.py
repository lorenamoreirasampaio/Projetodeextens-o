Sistema de Controle de Estoque - Loja de Saltos Femininos

import csv
import os
from datetime import datetime


class EstoqueInsuficienteError(Exception):
    pass


# ============================================================
# CLASSE PRODUTO
# ============================================================

class Produto:

    def __init__(self, codigo, nome, tamanho, preco, quantidade=0):
        self._codigo = codigo
        self._nome = nome
        self._tamanho = tamanho
        self._preco = float(preco)
        self._quantidade = int(quantidade)

    @property
    def codigo(self):
        return self._codigo

    @property
    def nome(self):
        return self._nome

    @property
    def tamanho(self):
        return self._tamanho

    @property
    def preco(self):
        return self._preco

    @property
    def quantidade(self):
        return self._quantidade

    def registrar_venda(self, qtd):
        if qtd > self._quantidade:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente. Disponível: {self._quantidade}"
            )
        self._quantidade -= qtd

    def repor_estoque(self, qtd):
        self._quantidade += qtd

    def to_dict(self):
        return {
            "codigo": self._codigo,
            "nome": self._nome,
            "tamanho": self._tamanho,
            "preco": self._preco,
            "quantidade": self._quantidade
        }

    def __str__(self):
        return (f"[{self._codigo}] {self._nome} | "
                f"Tam: {self._tamanho} | R$ {self._preco:.2f} | "
                f"Qtd: {self._quantidade}")


# ============================================================
# CLASSE ESTOQUE
# ============================================================

class Estoque:

    ARQUIVO = "produtos.csv"

    def __init__(self):
        self._produtos = {}
        self._carregar()

    def cadastrar(self, produto):
        if produto.codigo in self._produtos:
            raise ValueError(f"Código '{produto.codigo}' já existe.")
        self._produtos[produto.codigo] = produto
        self._salvar()

    def buscar(self, codigo):
        if codigo not in self._produtos:
            raise KeyError(f"Produto '{codigo}' não encontrado.")
        return self._produtos[codigo]

    def vender(self, codigo, qtd):
        produto = self.buscar(codigo)
        produto.registrar_venda(qtd)
        self._salvar()
        return produto.preco * qtd

    def repor(self, codigo, qtd):
        produto = self.buscar(codigo)
        produto.repor_estoque(qtd)
        self._salvar()

    def listar(self):
        return list(self._produtos.values())

    def _salvar(self):
        try:
            with open(self.ARQUIVO, "w", newline="", encoding="utf-8") as f:
                campos = ["codigo", "nome", "tamanho", "preco", "quantidade"]
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                for p in self._produtos.values():
                    writer.writerow(p.to_dict())
        except IOError as e:
            print(f"Erro ao salvar: {e}")

    def _carregar(self):
        if not os.path.exists(self.ARQUIVO):
            return
        try:
            with open(self.ARQUIVO, "r", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    p = Produto(row["codigo"], row["nome"], row["tamanho"],
                                row["preco"], row["quantidade"])
                    self._produtos[p.codigo] = p
        except IOError as e:
            print(f"Erro ao carregar: {e}")


# ============================================================
# INTERFACE CONSOLE
# ============================================================

def menu():
    print("\n==============================")
    print("  CONTROLE DE ESTOQUE")
    print("==============================")
    print("  1. Cadastrar produto")
    print("  2. Registrar venda")
    print("  3. Repor estoque")
    print("  4. Listar produtos")
    print("  0. Sair")
    print("==============================")
    return input("  Opção: ").strip()


def ler_inteiro(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("  Digite um número inteiro válido.")


def ler_float(msg):
    while True:
        try:
            return float(input(msg).replace(",", "."))
        except ValueError:
            print("  Digite um valor numérico válido.")


def op_cadastrar(estoque):
    print("\n-- CADASTRAR PRODUTO --")
    try:
        codigo   = input("  Código: ").strip().upper()
        nome     = input("  Nome: ").strip()
        tamanho  = input("  Tamanho: ").strip()
        preco    = ler_float("  Preço (R$): ")
        qtd      = ler_inteiro("  Quantidade inicial: ")

        estoque.cadastrar(Produto(codigo, nome, tamanho, preco, qtd))
        print("  ✔ Produto cadastrado!")
    except ValueError as e:
        print(f"  Erro: {e}")


def op_vender(estoque):
    print("\n-- REGISTRAR VENDA --")
    try:
        codigo = input("  Código do produto: ").strip().upper()
        qtd    = ler_inteiro("  Quantidade: ")
        total  = estoque.vender(codigo, qtd)
        print(f"  ✔ Venda registrada! Total: R$ {total:.2f}")
    except (KeyError, EstoqueInsuficienteError, ValueError) as e:
        print(f"  Erro: {e}")


def op_repor(estoque):
    print("\n-- REPOR ESTOQUE --")
    try:
        codigo = input("  Código do produto: ").strip().upper()
        qtd    = ler_inteiro("  Quantidade a repor: ")
        estoque.repor(codigo, qtd)
        print("  ✔ Estoque reposto!")
    except (KeyError, ValueError) as e:
        print(f"  Erro: {e}")


def op_listar(estoque):
    print("\n-- PRODUTOS --")
    produtos = estoque.listar()
    if not produtos:
        print("  Nenhum produto cadastrado.")
    else:
        for p in produtos:
            alerta = " ⚠ FALTA" if p.quantidade == 0 else ""
            print(f"  {p}{alerta}")


# ============================================================
# MAIN
# ============================================================

def main():
    estoque = Estoque()
    while True:
        opcao = menu()
        if opcao == "1":
            op_cadastrar(estoque)
        elif opcao == "2":
            op_vender(estoque)
        elif opcao == "3":
            op_repor(estoque)
        elif opcao == "4":
            op_listar(estoque)
        elif opcao == "0":
            print("\n  Sistema encerrado.\n")
            break
        else:
            print("  Opção inválida.")


if __name__ == "__main__":
    main()
