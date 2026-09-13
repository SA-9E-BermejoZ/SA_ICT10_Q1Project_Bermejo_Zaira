from datetime import datetime
from pyscript import document

# SKU Generator (index.html)

CATEGORY_CODES = {
    "Perishables": "PER",
    "Beverages": "BEV",
    "Disposables": "DIS",
    "Packaging": "PKG",
}


def _name_fragment(name):
    """Turn a product name into a 3-letter tag, e.g. 'Bottled Water' -> 'BOT'."""
    letters = "".join(ch for ch in name.upper() if ch.isalpha())
    if not letters:
        return "GEN"
    return letters[:3].ljust(3, "X")


def _check_digit(seed):
    """A small barcode-style check digit so two similar items don't collide."""
    total = sum(ord(ch) for ch in seed)
    return str(total % 97).zfill(2)


def SKU_generator(event=None):
    output = document.getElementById("sku_output")
    category = document.getElementById("category").value
    product_name = document.getElementById("product_name").value.strip()
    quantity_raw = document.getElementById("quantity").value.strip()

    if not product_name:
        output.innerHTML = (
            '<p class="stamp-alert">Enter a product name before stamping a code.</p>'
        )
        return

    try:
        quantity = int(quantity_raw)
        if quantity < 0:
            raise ValueError
    except ValueError:
        output.innerHTML = (
            '<p class="stamp-alert">Stock quantity needs to be a whole '
            "number, 0 or higher.</p>"
        )
        return

    cat_code = CATEGORY_CODES.get(category, "GEN")
    name_code = _name_fragment(product_name)
    qty_code = str(quantity).zfill(4)
    check = _check_digit(f"{cat_code}{name_code}{qty_code}{product_name}")
    sku = f"{cat_code}-{name_code}-{qty_code}-{check}"

    output.innerHTML = f"""
        <div class="output-panel">
            <span class="output-eyebrow">Generated code</span>
            <p class="sku-code">{sku}</p>
            <dl class="output-meta">
                <div><dt>Product</dt><dd>{product_name}</dd></div>
                <div><dt>Category</dt><dd>{category}</dd></div>
                <div><dt>On hand</dt><dd>{quantity} units</dd></div>
            </dl>
        </div>
    """


# Order ticket (receipt_generator.html)

MENU = [
    ("item1", "Americano"),
    ("item2", "Spanish Latte"),
    ("item3", "Cold Brew Malt"),
    ("item4", "Affogato"),
    ("item5", "Caramel Macchiato"),
]


def create_order(event=None):
    output = document.getElementById("show")
    chosen = []
    total = 0

    for item_id, label in MENU:
        box = document.getElementById(item_id)
        if box is not None and box.checked:
            price = int(box.value)
            chosen.append((label, price))
            total += price

    if not chosen:
        output.innerHTML = (
            '<p class="stamp-alert">Tap at least one item to ring up an order.</p>'
        )
        return


    lines = "".join(
        f'<div class="receipt-line"><span>{label}</span><span>\u20b1{price}</span></div>'
        for label, price in chosen
    )

    output.innerHTML = f"""
            {lines}
            <div class="receipt-total">
                <span>Total</span><span>\u20b1{total}</span>
            </div>
        </div>
    """
