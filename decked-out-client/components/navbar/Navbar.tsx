/* eslint-disable @next/next/no-img-element */
import Link from 'next/link';
import { useRouter } from 'next/router';
import styles from '/styles/modules/Navbar.module.scss';

const routes: string[] = [];

function Navlink({ route }: { route: string; }) {
    const router = useRouter();

    const path = `/${route}`;
    let active = false;
    if (route === 'home') {
        active = router.pathname == path || router.pathname == "/";
    } else {
        active = router.pathname == path;
    }

    return (
        <Link
            className={active ? styles.activeLink : undefined}
            href={`/${route}`}
        >
            {route.charAt(0).toUpperCase() + route.slice(1)}
        </Link>
    );
}

function Navbar() {

    return (
        <div className={styles.navContainer}>
            <img src="/icon.png" alt="helo" />
            <Link className={styles.activeLink} href="/">Decked Out</Link>
            {routes.map((route, i) => <Navlink route={route} key={i} />)}
        </div>
    );
}

export default Navbar;